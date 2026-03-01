import os
import re
import logging
from typing import Dict, Optional
from mistralai import Mistral
import json

logger = logging.getLogger(__name__)


class AnimationGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")
        
        self.client = Mistral(api_key=self.api_key)
        self.model = "devstral-medium-latest"
    
    def generate_animation(self, prompt: str) -> Dict[str, str]:
        try:
            #Planner agent
            planner_prompt = """Your job is to create a more clear and detailed query, for an 
            agent that generates educational and interactive animations using html + css + js, 
            based on the user's query.
            Anser with a json with the following fields:
            - reasoning: str
            - improved_query: str
            - plan: str

            Do it in 2 steps:
            Step 1: Check if the user query already especifies what to draw/animate.
            - If so:
            -- Just improve the query.
            - If not:
            -- Create a query that especifies what to draw/animate that better answers the user's query.
            -- Create the explanantion like a Phd/expert would explain to a teenager - as sophiscated/deep as possible but simple to understand.
            -- According to the topic, choose the the explanation of one of the following:
            --- Physics, chemistry - Richard Feynman, Carl Sagan;
            --- Astronomy, Astrophysics, Cosmology - Neil deGrasse Tyson;
            --- Biology - Carl Sagan;

            Step 2: Using the improved query from step 1, describe the scene, elements, how they look and how they behave in the field 'plan'. Don't use more than 300 characters.
            - Take care of the scientific details (the physics) of the scene.
            - When relevant, add controls for some features of the animation. For example, if the user asks for a planet, add controls for the planet's rotation, zoom, etc.
            - If an image is provided as scene reference, is to create a similar scene using svg.
            - Focus on educational value and clarity, assuming your audience is a teenager (13-18 years old).
            - Make sure there's a text section explaining what's happening in the animation, step by step.
            - All the text must be in the same language as the user's query.
            - Be concise - avoid visual noise so the user has a minimal information that is easy to digest.
            """
            print("Prompt: ", prompt)
            planner_response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": planner_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                #max_tokens=4000
            )
            
            planner_output = planner_response.choices[0].message.content
            planner_output = planner_output.replace("```json", "").replace("```", "")
            planner_json = json.loads(planner_output)
            improved_query = planner_json["improved_query"]
            plan = planner_json["plan"]

            #HTML creator agent
            system_prompt = """You are an expert web animation developer. Your task is to create self-contained HTML files with CSS and JavaScript animations based on user descriptions.

Follow these guidelines:
1. Create a complete, valid HTML5 document with embedded CSS and JavaScript
2. Use semantic HTML and best practices
3. Ensure the animation is responsive and works on different screen sizes
4. Use modern JavaScript (ES6+) and CSS3
5. Make animations visually appealing with proper colors, timing, and easing

Return ONLY the HTML code with embedded CSS and JavaScript. Do not include any explanations, markdown formatting, or additional text outside the HTML code."""
            user_prompt = f"""Create an animation based on the following plan:'''
            {plan}'''"""
            
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1,
                #max_tokens=4000
            )
            
            html_content = response.choices[0].message.content
            html_content = html_content.replace("```html", "").replace("```", "")
            
            if not html_content:
                raise ValueError("Failed to extract valid HTML from response")
            
            return {
                "status": "success",
                "html_content": html_content,
                "model_used": self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating animation: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "html_content": ""
            }