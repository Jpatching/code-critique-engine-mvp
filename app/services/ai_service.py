"""
AI Analysis Service

This module handles all interactions with AI providers for code analysis.
Provides concurrent processing, error handling, and response validation.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional
import google.generativeai as genai
from google.generativeai import types

from app.config import config


class AIAnalysisService:
    """Service for AI-powered code analysis"""
    
    def __init__(self):
        self.model_name = self._get_available_model()
        self._configure_client()
    
    def _configure_client(self):
        """Configure the AI client"""
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
            print(f"AI client initialized with model: {self.model_name}")
        else:
            raise ValueError("GEMINI_API_KEY is required but not set")
    
    def _get_available_model(self) -> str:
        """Get the best available model for the current configuration"""
        if config.FORCE_FREE_TIER:
            return self._get_free_tier_model()
        return self._discover_best_model()
    
    def _get_free_tier_model(self) -> str:
        """Get the best free-tier model"""
        free_tier_models = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-2.5-flash',
            'models/gemini-pro'
        ]
        
        try:
            available_models = {m.name: m for m in genai.list_models()}
            
            for model_name in free_tier_models:
                if model_name in available_models:
                    model = available_models[model_name]
                    if 'generateContent' in model.supported_generation_methods:
                        return model_name
                        
            return 'models/gemini-pro'  # Fallback
            
        except Exception as e:
            print(f"Error discovering models: {e}")
            return 'models/gemini-pro'
    
    def _discover_best_model(self) -> str:
        """Discover the best available model"""
        try:
            models = genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    return model.name
            return 'models/gemini-pro'
        except Exception as e:
            print(f"Error discovering models: {e}")
            return 'models/gemini-pro'
    
    def analyze_code(self, prompt: str, code: str, project_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze code using AI with concurrent processing and optional project context
        
        Args:
            prompt: The original AI prompt
            code: The code to analyze
            project_context: Optional project context string with architecture info
            
        Returns:
            Dictionary containing analysis results
        """
        prompt_data = {
            'prompt': prompt, 
            'code': code,
            'project_context': project_context or ''
        }
        
        # Use ThreadPoolExecutor for concurrent AI calls
        with ThreadPoolExecutor(max_workers=config.MAX_CONCURRENT_AI_REQUESTS) as executor:
            
            # Submit all three analysis tasks
            future_scores = executor.submit(self._call_ai, self._get_scores_prompt(), prompt_data)
            future_reports = executor.submit(self._call_ai, self._get_reports_prompt(), prompt_data)
            future_refactor = executor.submit(self._call_ai, self._get_refactor_prompt(), prompt_data)
            
            try:
                # Get results from all futures
                scores_result = future_scores.result()
                reports_result = future_reports.result()
                refactor_result = future_refactor.result()
                
                # Combine and process results
                return self._combine_results(scores_result, reports_result, refactor_result, code)
                
            except Exception as e:
                raise Exception(f"AI analysis failed: {str(e)}")
    
    def _call_ai(self, prompt_template: str, prompt_data: Dict[str, str]) -> str:
        """
        Make a single AI API call with error handling
        
        Args:
            prompt_template: The prompt template to use
            prompt_data: Data to fill the template
            
        Returns:
            JSON string response from AI
        """
        final_prompt = prompt_template.format(**prompt_data)
        
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                final_prompt,
                generation_config=types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            raw_text = response.text.strip()
            
            # Clean markdown fences if present
            if raw_text.startswith('```json'):
                raw_text = raw_text[len('```json'):].strip()
            if raw_text.endswith('```'):
                raw_text = raw_text[:-3].strip()
            
            # Ensure valid UTF-8
            raw_text = raw_text.encode('utf-8', 'ignore').decode('utf-8')
            
            # Validate JSON
            try:
                parsed = json.loads(raw_text)
                return json.dumps(parsed, ensure_ascii=False)
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                cleaned = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw_text)
                parsed = json.loads(cleaned)
                return json.dumps(parsed, ensure_ascii=False)
                
        except Exception as e:
            print(f"AI API call failed: {e}")
            return json.dumps({"error": f"AI API Error: {e}"})
    
    def _combine_results(self, scores: str, reports: str, refactor: str, original_code: str) -> Dict[str, Any]:
        """
        Combine results from all AI analysis calls
        
        Args:
            scores: JSON string with scores and explanations
            reports: JSON string with detailed reports
            refactor: JSON string with refactored code and roadmap
            original_code: Original code for comparison
            
        Returns:
            Combined analysis results
        """
        combined = {}
        
        try:
            # Parse and merge scores
            scores_data = json.loads(scores)
            combined.update(scores_data)
            
            # Parse and merge reports (flatten nested structure)
            reports_data = json.loads(reports)
            if 'report' in reports_data and isinstance(reports_data['report'], dict):
                combined.update(reports_data['report'])
            
            # Parse and merge refactor results
            refactor_data = json.loads(refactor)
            combined.update(refactor_data)
            
            # Process project roadmap (convert string to array)
            if 'project_roadmap' in combined and isinstance(combined['project_roadmap'], str):
                roadmap_steps = [
                    step.strip() for step in combined['project_roadmap'].split('\n') 
                    if step.strip()
                ]
                combined['project_roadmap'] = roadmap_steps
            
            # Add original code for comparison
            combined['original_code'] = original_code
            
            # Ensure explanation_summary exists (frontend compatibility)
            if 'explanation' in combined and 'explanation_summary' not in combined:
                combined['explanation_summary'] = combined.pop('explanation')
            
            return combined
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response: {e}")
        except Exception as e:
            raise Exception(f"Failed to combine AI results: {e}")
    
    def _get_scores_prompt(self) -> str:
        """Get the prompt template for scores and explanations"""
        return """
You are an expert AI Code Reviewer. Your task is to perform an analysis of the provided AI-generated CODE based on the ORIGINAL AI PROMPT.

{project_context}

Your output MUST be a JSON object with the following five keys:
1.  "total_score" (INTEGER out of 25)
2.  "reliability_score" (INTEGER out of 10)
3.  "mastery_score" (INTEGER out of 15)
4.  "explanation_summary" (STRING, a high-level overview of the code's logic, data structures, and time complexity.)
5.  "debug_prognosis" (STRING, the single most likely logic error or bug the user will face, why it fails, and the EXACT FIX.)

The CODE to analyze is provided below. Ensure your output is ONLY the raw JSON object.

ORIGINAL AI PROMPT: {prompt}
CODE: {code}
"""
    
    def _get_reports_prompt(self) -> str:
        """Get the prompt template for detailed reports"""
        return """
You are an expert team of Code Review specialists. Your task is to analyze the provided CODE and generate five detailed, independent reports.

{project_context}

Your output MUST be a JSON object with a single key, "report", which is an object containing the following five keys, each mapped to a STRING report:
1.  "clarity" (Detailed review of variable naming, casing, and readability.)
2.  "modularity" (Detailed review of function breakdown and reusability.)
3.  "efficiency" (Detailed review of algorithm choice and complexity for the given task.)
4.  "security" (Analysis from a Security Analyst perspective.)
5.  "documentation" (Analysis from a Documentation Specialist perspective.)

The CODE to analyze is provided below. Ensure your output is ONLY the raw JSON object.

CODE: {code}
"""
    
    def _get_refactor_prompt(self) -> str:
        """Get the prompt template for refactoring and roadmap"""
        return """
You are an expert Software Architect. Your task is to analyze the provided CODE and ORIGINAL AI PROMPT and provide a long-term architectural solution.

{project_context}

Your output MUST be a JSON object with the following two keys:
1.  "refactored_code" (STRING, the complete, production-ready, refactored Python code that solves all major issues from the reports, including security and file handling where applicable. The code MUST be ready to copy-paste.)
2.  "project_roadmap" (STRING, a 3-5 step architectural plan for the developer to scale this code into a larger project, focusing on module separation, external configuration, and system initialization. Start with 'Your Architectural Next Steps:').

The CODE to analyze is provided below. Ensure your output is ONLY the raw JSON object.

ORIGINAL AI PROMPT: {prompt}
CODE: {code}
"""