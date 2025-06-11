from dotenv import load_dotenv
import os
import aiohttp
import asyncio
from typing import Dict, Optional, Required
import polars as pl
from utils import SolParams, ManifestParams
import time
import json

# Load environment variables
load_dotenv()

# Class for accessing NASA's API
class RoverAPI:
    # Define different types of cameras and rovers
    CAMERAS = {
        'curiosity': ['FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM'],
        'opportunity': ['FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES'],
        'spirit': ['FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES']
    }
    ROVERS = ['curiosity', 'opportunity', 'spirit']

    # Class vars
    def __init__(self):
        self.api_key = os.getenv('API_KEY', 'DEMO_KEY')
        self.base_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers"


    #
    # MANIFEST FUNCTIONS TO GAIN INFO ON ROVERS/CAMERAS/SOL'S BEFORE PHOTO QUERYING
    #

    # Get manifest parameters
    def get_manifest_params(self, rover: str) -> ManifestParams:
        base_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}"
        params = {'api_key': self.api_key}
        return base_url, params
    
    async def get_manifest(self, rover: str, session: aiohttp.ClientSession) -> Dict:
        base_url, params = self.get_manifest_params(rover)
        data = await self.make_request(url=base_url, params=params, session=session)
        print(f"Manifest data for {rover} successfully pulled")
        return data
    

    # 
    # General request function
    #
    async def make_request(self, url: str, params: Optional[Dict], session: aiohttp.ClientSession) -> Dict:
        for attempt in range(3):
            # Try request
            try:
                # Async get request
                async with session.get(url=url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    # Check status code
                    if resp.status == 200:
                        # Await data from response and return
                        data = await resp.json(content_type=None)
                        return {'data': data['photo_manifest'], 'url': str(resp.url), 'status_code': resp.status}
                    else:
                        # Return an error message 
                        error_text = await resp.json(content_type=None)
                        return {'url': str(resp.url), 'status_code': resp.status, 'error': error_text}
            # Return exception when 1st try 
            except Exception as e:
                if attempt == 2:
                    return {'error_msg': f"Request failed after 3 attempts: {e}"}
                else:
                    print(f"Attempt {attempt + 1} failed, retrying in 2s: {e}")
                    await asyncio.sleep(2)
            
# Event loop to init api and make requests 
async def main():
    api = RoverAPI()
    start_time = time.time()

    # Start session in main loop so all requests are pulled using 1 client
    async with aiohttp.ClientSession() as session:
        curiosity, opportunity, spirit = await asyncio.gather(
            api.get_manifest(rover=api.ROVERS[0], session=session), # Curiosity
            api.get_manifest(rover=api.ROVERS[1], session=session), # Opportunity
            api.get_manifest(rover=api.ROVERS[2], session=session)  # Spirit
        )

    # Store concurrent tasks
    manifest_data = {
        'curiosity_manifest_data': curiosity,
        'opportunity_manifest_data': opportunity,
        'spirit_manifest_data': spirit
    }

    # Calculate time taken and display
    elapsed_time = time.time() - start_time
    print(f"Time taken: {elapsed_time:.2f}s")
    
    # Store to output files
    path = 'output_files/manifest_data.json'
    with open(path, 'w') as f:
        json.dump(manifest_data, f, indent=4)
    print(f"Data successfully saved to {path}")


if __name__ == '__main__':
    asyncio.run(main())