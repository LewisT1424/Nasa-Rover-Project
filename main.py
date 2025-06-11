from dotenv import load_dotenv
import os
import aiohttp
import asyncio
from typing import Dict, Optional, Required
import polars as pl

load_dotenv()

class RoverAPI:
    # Define different types of cameras and rovers
    CAMERAS = {
        'curiosity': ['FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM'],
        'opportunity': ['FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES'],
        'spirit': ['FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES']
    }
    ROVERS = ['curiosity', 'opportunity', 'spirit']

    def __init__(self):
        self.api_key = os.getenv('API_KEY', 'DEMO_KEY')
        self.base_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers"


    #
    # MANIFEST FUNCTIONS TO GAIN INFO ON ROVERS/CAMERAS/SOL'S BEFORE PHOTO QUERYING
    #

    # Get manifest parameters
    def get_manifest_params(self, rover):
        base_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}"
        params = {'api_key': self.api_key}
        return base_url, params
    
    async def get_manifest(self, rover=Required[str]) -> Dict:
        base_url, params = self.get_manifest_params(rover)
        data = await self.make_request(url=base_url, params=params)
        return data
    

    # 
    # General request function
    #

    async def make_request(self, url: str, params: Optional[Dict]) -> Dict:
        # Run with async client
        async with aiohttp.ClientSession() as session:
            # Try request
            try:
                # Async get request
                async with session.get(url=url, params=params) as resp:
                    # Check status code
                    if resp.status == 200:
                        # Await data from response and return
                        data = await resp.json(content_type=None)
                        return {'data': data['photo_manifest'], 'url': resp.url, 'status_code': resp.status}
                    else:
                        # Return an error message 
                        error_text = await resp.json(content_type=None)
                        return {'url': str(resp.url), 'status_code': resp.status, 'error': error_text}
            # Return exception when 1st try 
            except Exception as e:
                return {'error_msg': f"Request Failed: {e}"}
            

async def main():
    api = RoverAPI()
    manifest_data = await api.get_manifest(rover=api.ROVERS[2])
    print(manifest_data)

if __name__ == '__main__':
    asyncio.run(main())