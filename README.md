# NASA Mars Rover API Client

A Python async client for fetching mission manifest data from NASA's Mars Rover Photos API. This tool retrieves detailed information about the Curiosity, Opportunity, and Spirit rovers including their mission status, landing dates, photo counts, and available cameras.

## Features

- ✅ **Async HTTP requests** for fast concurrent data fetching
- 🔄 **Automatic retry logic** with exponential backoff
- 🚀 **Multi-rover support** (Curiosity, Opportunity, Spirit)
- 📄 **JSON export** functionality
- 🔑 **Environment variable configuration**
- 🛡️ **Type safety** with TypedDict annotations
- ⏱️ **Performance timing** and logging

## Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:LewisT1424/Nasa-Rover-Project.git
   cd mars-rover-api-client
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_nasa_api_key_here
   ```
   
   Get your free API key from [api.nasa.gov](https://api.nasa.gov)

## Usage

### Basic Usage

Run the script to fetch manifest data for all rovers:

```bash
python manifest-scripts/fetch_manifest_data.py
```

This will:
- Fetch manifest data for Curiosity, Opportunity, and Spirit rovers
- Display timing information and success/failure status
- Save results to `output_files/manifest_data.json`

### Example Output

```
Manifest data for curiosity successfully pulled
Manifest data for opportunity successfully pulled  
Manifest data for spirit successfully pulled
Time taken: 42.16s
Data successfully saved to output_files/manifest_data.json
```

## File Structure

```
mars-rover-api-client/
├── manifest-scripts
│   └── fetch_manifest_data.py # Main application script
│   └── manifest_analysis.ipynb.py # Notebook to analyse results from fetching manifest
├── utils.py               # Type definitions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── output_files/          # Generated JSON files (created automatically)
│   └── manifest_data.json
└── README.md             # This file
```

## Dependencies

- **aiohttp** - Async HTTP client for API requests
- **python-dotenv** - Environment variable management
- **polars** - Data manipulation and analysis inside notebooks

See `requirements.txt` for specific versions.

## API Information

This client uses NASA's Mars Rover Photos API:
- **Base URL**: `https://api.nasa.gov/mars-photos/api/v1/`
- **Rate Limits**: 1,000 requests per hour with API key
- **Documentation**: [NASA API Docs](https://api.nasa.gov)

### Manifest Data Includes

- Rover name and mission status
- Landing and launch dates
- Total number of photos taken
- Most recent Sol (Martian day) with photos
- Available cameras for each Sol
- Photo count breakdowns by Sol

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | NASA API key | `DEMO_KEY` |

### Rover Support

| Rover | Status | Cameras Supported |
|-------|--------|-------------------|
| Curiosity | Active | FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM |
| Opportunity | Complete | FHAZ, RHAZ, NAVCAM, PANCAM, MINITES |
| Spirit | Complete | FHAZ, RHAZ, NAVCAM, PANCAM, MINITES |

## Error Handling

The client includes robust error handling:

- **Automatic retries** (3 attempts with 2-second delays)
- **Timeout protection** (15-second request timeout)
- **SSL error handling** for NASA API connectivity issues
- **Graceful degradation** if individual rovers fail

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| SSL timeout | NASA API server issues | Wait and retry, or use sequential requests |
| 403 Forbidden | Invalid API key | Check your API key in `.env` file |
| Rate limiting | Too many requests | Wait or get a higher-limit API key |

## Example JSON Output

```json
{
    "curiosity_manifest_data": {
        "data": {
            "name": "Curiosity",
            "landing_date": "2012-08-06",
            "launch_date": "2011-11-26", 
            "status": "active",
            "max_sol": 4331,
            "max_date": "2025-01-15",
            "total_photos": 695670,
            "photos": [...]
        },
        "status_code": 200
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NASA for providing the Mars Rover Photos API
- Mars rover mission teams for the incredible data