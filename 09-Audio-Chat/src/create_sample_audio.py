"""
Create sample audio files for testing the audio chat application
"""

import os
import wave
import numpy as np
from pathlib import Path

def create_tone_wav(filename: str, frequency: float = 440, duration: float = 2.0, sample_rate: int = 44100):
    """Create a simple WAV file with a tone."""
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate sine wave
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Add some modulation to make it more interesting
    modulation = np.sin(2 * np.pi * 2 * t) * 0.3
    audio_data = audio_data * (1 + modulation)
    
    # Normalize and convert to 16-bit
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_sample_scenarios():
    """Create sample audio files representing different customer scenarios."""
    # Create data directory
    data_dir = Path("../data/audio_samples")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    scenarios = [
        {
            "filename": "customer_order.wav",
            "frequency": 440,  # A4
            "duration": 3.0,
            "description": "Customer placing an order for fresh vegetables"
        },
        {
            "filename": "quality_concern.wav",
            "frequency": 330,  # E4 (lower tone for concern)
            "duration": 2.5,
            "description": "Customer reporting quality issues with delivered produce"
        },
        {
            "filename": "delivery_inquiry.wav",
            "frequency": 523,  # C5 (higher tone for inquiry)
            "duration": 2.0,
            "description": "Customer asking about delivery schedules"
        },
        {
            "filename": "product_availability.wav",
            "frequency": 392,  # G4
            "duration": 2.5,
            "description": "Customer checking availability of seasonal fruits"
        }
    ]
    
    print("Creating sample audio files...")
    
    for scenario in scenarios:
        filepath = data_dir / scenario["filename"]
        create_tone_wav(
            str(filepath),
            frequency=scenario["frequency"],
            duration=scenario["duration"]
        )
        
        # Create accompanying text file with description
        txt_filepath = data_dir / scenario["filename"].replace(".wav", ".txt")
        with open(txt_filepath, 'w') as f:
            f.write(scenario["description"])
        
        print(f"Created: {scenario['filename']} - {scenario['description']}")
    
    # Create a README for the audio samples
    readme_path = data_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write("# Sample Audio Files\n\n")
        f.write("These are placeholder audio files for testing the audio chat application.\n")
        f.write("In a real scenario, these would contain actual speech recordings.\n\n")
        f.write("## Files:\n\n")
        
        for scenario in scenarios:
            f.write(f"- **{scenario['filename']}**: {scenario['description']}\n")
            f.write(f"  - Frequency: {scenario['frequency']} Hz\n")
            f.write(f"  - Duration: {scenario['duration']} seconds\n\n")
    
    print(f"\nSample audio files created in: {data_dir}")
    print("Note: These are placeholder tones. In production, use actual speech recordings.")

if __name__ == "__main__":
    create_sample_scenarios()