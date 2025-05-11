from dotenv import load_dotenv
from typing import List, Dict, Optional, Any
import logging
import json
import asyncio

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, google, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalIntakeAssistant(Agent):
    def __init__(self) -> None:
        # Create a system prompt that focuses on the specific workflow
        system_prompt = """
        You are MediAssist, a medical intake assistant. Follow these exact steps in order:
        
        STEP 1: Ask the patient to upload a picture of their insurance card.
        STEP 2: Ask the patient why they are visiting the doctor today, asking for detailed symptoms.
        STEP 3: Ask if the patient has any additional information they'd like to share.
        
        Follow ONLY these steps in this EXACT order.
        Do not ask for any other information not specified in these steps.
        Do not create additional questions.
        After each question, wait for the user's response before proceeding.
        """
        
        super().__init__(instructions=system_prompt)
        
        self.current_step = 0
        self.patient_data = {
            "insurance_card": None,
            "visit_reason": None,
            "additional_info": None
        }
        self.conversation_started = False
        
    async def on_message(self, message) -> None:
        logger.info(f"Processing message. Current step: {self.current_step}")
        
        # If this is the first message from the user and we haven't started the conversation
        if not self.conversation_started:
            self.conversation_started = True
            logger.info("First user message received, asking first question (insurance card)")
            await self.process_step_1()
            return
            
        if self.current_step == 0:
            # After user responds to insurance card request
            await self.dummy_process_insurance_image(message.text)
            self.current_step += 1
            await self.process_step_2()
        
        elif self.current_step == 1:
            # After user explains reason for visit
            visit_reason_summary = await self.summarize_text(message.text)
            self.patient_data["visit_reason"] = visit_reason_summary
            self.current_step += 1
            await self.process_step_3()
        
        elif self.current_step == 2:
            # After user provides additional information
            additional_info_summary = await self.summarize_text(message.text)
            self.patient_data["additional_info"] = additional_info_summary
            self.current_step += 1
            await self.finish_intake()
        
    async def process_step_1(self) -> None:
        """Ask the user to upload their insurance card"""
        logger.info("Asking for insurance card upload")
        
        await self.session.generate_reply(
            instructions="""
            Ask the patient to upload a picture of their insurance card.
            Explain this will help with processing their visit efficiently.
            """
        )
    
    async def dummy_process_insurance_image(self, response: str) -> None:
        """Dummy function to simulate processing an insurance card image"""
        logger.info("Processing insurance card (dummy function)")
        # In a real implementation, this would process an actual image
        # For now, we'll just store the user's response
        self.patient_data["insurance_card"] = {
            "received": True,
            "user_response": response
        }
    
    async def process_step_2(self) -> None:
        """Ask the patient why they are visiting"""
        logger.info("Asking for reason of visit")
        
        await self.session.generate_reply(
            instructions="""
            Thank the patient for providing their insurance information.
            Now ask them to explain in detail why they are visiting the doctor today.
            Encourage them to describe their symptoms thoroughly.
            """
        )
    
    async def process_step_3(self) -> None:
        """Ask if the patient has anything else to add"""
        logger.info("Asking for additional information")
        
        await self.session.generate_reply(
            instructions="""
            Thank the patient for explaining their symptoms.
            Ask if there's anything else they would like to add or share that might be relevant to their visit.
            """
        )
    
    async def summarize_text(self, text: str) -> str:
        """Summarize the user's response"""
        logger.info("Summarizing user response")
        
        try:
            # Use the same OpenAI client to generate a summary
            summary_prompt = f"Please summarize the following patient response into a concise medical note: '{text}'"
            
            # In a real implementation, this would call the OpenAI API directly
            # For now, we'll create a simple summary by truncating
            if len(text) > 100:
                summary = text[:97] + "..."
            else:
                summary = text
                
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return text[:100] + "..." if len(text) > 100 else text
    
    async def finish_intake(self) -> None:
        """Finish the intake process and output the collected data"""
        logger.info("Finishing intake process")
        
        # Print the JSON data to verify it's working
        json_output = json.dumps(self.patient_data, indent=2)
        print("\n=== PATIENT INTAKE DATA ===")
        print(json_output)
        print("==========================\n")
        
        # Send final message to the user
        await self.session.generate_reply(
            instructions="""
            Thank the patient for providing all the information.
            Let them know their information has been recorded and will be shared with their doctor.
            Tell them that a medical professional will be with them shortly.
            """
        )
        
        # End the session after sending the final message
        logger.info("Attempting to end session")
        try:
            # Add a small delay to ensure the final message is delivered
            await asyncio.sleep(3)
            
            # Try multiple ways to end the session
            if hasattr(self.session, 'stop'):
                await self.session.stop()
                logger.info("Session stopped via stop() method")
            
            # Force exit the process as a fallback
            print("Session completed - forcing program exit in 5 seconds...")
            await asyncio.sleep(5)
            import os
            import sys
            os._exit(0)  # Force exit the process
            
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            print("Error during session termination, forcing exit...")
            import os
            import sys
            await asyncio.sleep(2)
            os._exit(0)  # Force exit even if there was an error


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=google.STT(),
        llm=openai.LLM(model="gpt-4o-2024-11-20"),  # Using the most capable model
        tts=openai.TTS(model="gpt-4o-mini-tts"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    assistant = MedicalIntakeAssistant()
    logger.info("Initializing MedicalIntakeAssistant")
    
    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Send initial greeting
    logger.info("Sending initial greeting")
    await session.generate_reply(
        instructions="""
        Greet the user briefly as MediAssist, a medical intake assistant.
        Explain that you'll be helping them complete their intake process before seeing the doctor.
        Mention that all information is confidential and will be shared only with their healthcare team.
        Wait for the user's response before beginning the intake questions.
        """
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))