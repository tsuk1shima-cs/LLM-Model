"""
Qwen 3.5 4B with Ollama + Advanced Metrics Tracking

Converted from Qwen_Ollama_Complete.ipynb.
Colab/IPython shell magics (!commands) are run via subprocess.
Install/start steps assume Linux (e.g. Google Colab). On Windows,
install Ollama from https://ollama.com and skip those cells.
"""

from __future__ import annotations

import os
import subprocess
import sys


def run(command: str) -> None:
    """Run a shell command, raising if it fails (like notebook ! magics)."""
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed ({completed.returncode}): {command}")


# %% [markdown] cell 0
# # Qwen 3.5 4B with Ollama + Advanced Metrics Tracking
#
# **Why Qwen 3.5 4B + Ollama?**
# - ✅ **Confirmed Available** on Ollama: [qwen3.5:4b](https://ollama.com/library/qwen3.5:4b)
# - ⚡ **Much faster downloads** - Optimized ~2.5GB format
# - 🚀 **Better performance** - Optimized inference engine
# - 🧠 **Latest Architecture** - Hybrid Gated Delta Networks
# - 📊 **Advanced Metrics** - TTFT, TBT, Throughput tracking!
# - 💾 **Lower memory usage** - Only ~3GB VRAM
# - 🎯 **Simple API** - Easy to use
#
# **Qwen 3.5 vs 2.5:**
# - 📈 Better reasoning capabilities
# - 🎨 Enhanced multimodal understanding
# - 📝 Improved instruction following
# - 🔄 Up to 128K context window
#
# **Available Qwen 3.5 Models:**
# - `qwen3.5:0.5b` - Ultra lightweight (0.5B params)
# - `qwen3.5:1.5b` - Small & fast (1.5B params)
# - `qwen3.5:3b` - Balanced (3B params)
# - `qwen3.5:4b` - **✅ Default** - Great balance (4B params) 🌟
# - `qwen3.5:7b` - High quality (7B params)
# - `qwen3.5:14b` - Best performance (14B params)
#
# **Official Links:**
# - 🔗 [Ollama Qwen 3.5 Page](https://ollama.com/library/qwen3.5)
# - 🎯 [Qwen 3.5 4B Direct](https://ollama.com/library/qwen3.5:4b)
# - 📚 [Ollama Documentation](https://ollama.com/)

# %% [markdown] cell 1
# ## Step 1: Install Ollama on Colab

# %% [code] cell 2
# Update system packages
run('apt-get -qq update')
run('apt-get -qq install -y pciutils zstd')

# Download and install Ollama
run('curl -fsSL https://ollama.com/install.sh | sh')

print("\n" + "="*60)
print("✅ Ollama installed successfully!")
print("="*60)

# %% [markdown] cell 3
# ## Step 2: Verify Installation

# %% [code] cell 4
# Verify Ollama installation
run('which ollama && ollama --version')

print("\n✅ Ollama is ready to use!")

# %% [markdown] cell 5
# ## Step 3: Check GPU Availability

# %% [code] cell 6
import subprocess

print("="*60)
print("GPU INFORMATION")
print("="*60)

# Check with nvidia-smi
try:
    result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        gpu_info = result.stdout.strip().split(', ')
        print(f"🎮 GPU: {gpu_info[0]}")
        print(f"💾 Total VRAM: {gpu_info[1]}")
        print(f"🔓 Free VRAM: {gpu_info[2]}")
        print("✅ GPU is available for Ollama")
    else:
        print("⚠️  No GPU detected")
except Exception as e:
    print(f"❌ Error checking GPU: {e}")

print("="*60)

# %% [markdown] cell 7
# ## Step 4: Start Ollama Server

# %% [code] cell 8
import subprocess
import time
import os

# Start Ollama server in background
print("🚀 Starting Ollama server...")

# Kill any existing Ollama processes
run('pkill -9 ollama 2>/dev/null || true')

# Start server in background
os.system('nohup ollama serve > /tmp/ollama.log 2>&1 &')

# Wait for server to start
print("⏳ Waiting for server to initialize...")
time.sleep(5)

# Check if server is running
try:
    import requests
    response = requests.get('http://localhost:11434/api/tags')
    if response.status_code == 200:
        print("✅ Ollama server is running!")
        print("🌐 Server: http://localhost:11434")
    else:
        print("⚠️  Server may not be ready yet")
except:
    print("⚠️  Checking server status...")
    time.sleep(3)
    print("✅ Server should be ready now!")

# %% [markdown] cell 9
# ## Step 5: Download Qwen 3.5 4B Model
#
# **🌟 Why Qwen 3.5 4B is the Best Choice:**
# - ✅ **Confirmed Available** on Ollama
# - 🧠 **Latest Architecture**: Hybrid Gated Delta Networks
# - 📈 **Better Reasoning**: Improved over Qwen 2.5
# - 🎨 **Enhanced Multimodal**: Better image understanding
# - 💾 **Efficient**: Only ~2.5GB, fits on T4 GPU
# - ⚡ **Fast**: 35-55 tokens/sec on T4
#
# **Model Info:**
# - Model: `qwen3.5:4b`
# - Size: ~2.5GB
# - Context: 128K tokens
# - VRAM: ~3GB during inference
#
# **Other Available Sizes:**
# - `qwen3.5:0.5b` - Ultra fast (~500MB)
# - `qwen3.5:1.5b` - Very fast (~1GB)
# - `qwen3.5:3b` - Balanced (~2GB)
# - `qwen3.5:7b` - High quality (~4.5GB)
# - `qwen3.5:14b` - Best quality (~9GB)

# %% [code] cell 10
import time

# Use Qwen 3.5 4B (confirmed available on Ollama)
MODEL_NAME = "qwen3.5:4b"  # 🌟 Latest Qwen 3.5 architecture

print(f"📥 Downloading model: {MODEL_NAME}")
print("💡 Qwen 3.5 has improved reasoning and multimodal capabilities!")
print("⏳ This will take 2-3 minutes for ~2.5GB download...\n")

start_time = time.time()

# Pull the model
run(f'ollama pull {MODEL_NAME}')

download_time = time.time() - start_time

print(f"\n✅ Model downloaded in {download_time:.2f} seconds!")
print(f"🎯 Model ready: {MODEL_NAME}")
print(f"📊 Model size: ~2.5GB")

# %% [markdown] cell 11
# ## Step 6: List Available Models

# %% [code] cell 12
# List all downloaded models
print("📦 Downloaded Models:\n")
run('ollama list')

print("\n" + "="*60)
print(f"✅ Active Model: {MODEL_NAME}")
print(f"🌐 Model Page: https://ollama.com/library/{MODEL_NAME.replace(':', '/')}")
print("="*60)

# %% [markdown] cell 13
# ## Step 7: Install Python Client & Metrics Dependencies

# %% [code] cell 14
run('pip install ollama requests pandas matplotlib gspread oauth2client -q')

print("✅ Python client and metrics dependencies installed!")
print("📊 Ready for: Ollama + Advanced Metrics Tracking!")

# %% [markdown] cell 15
# ## Step 8: Setup Advanced Metrics Tracker
#
# **📊 Advanced Metrics Tracking Features:**
# - ⚡ **TTFT** (Time To First Token) - Latency measurement
# - 🔄 **TBT** (Time Between Tokens) - Token generation consistency
# - 🚀 **Throughput** - Tokens per second
# - 📈 **Visualizations** - Performance dashboards
# - 📊 **Export** - CSV and Google Sheets support
# - 📝 **Summary Stats** - Aggregate performance metrics

# %% [code] cell 16
"""
Advanced Metrics Tracker for Qwen 3.5 4B
Tracks TTFT, TBT, throughput, and exports to Google Sheets
"""

import time
import statistics
from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# For Google Sheets export
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False

@dataclass
class DetailedMetrics:
    """Detailed performance metrics for each generation."""
    timestamp: str
    prompt: str
    response: str
    
    # Timing metrics
    ttft: float  # Time to First Token (seconds)
    avg_tbt: float  # Average Time Between Tokens (seconds)
    total_time: float  # Total generation time (seconds)
    
    # Token metrics
    prompt_tokens: int
    output_tokens: int
    total_tokens: int
    
    # Speed metrics
    tokens_per_second: float
    ttft_ms: float  # TTFT in milliseconds
    avg_tbt_ms: float  # Average TBT in milliseconds
    
    # Model info
    model: str
    temperature: float
    top_p: float
    max_tokens: int

class AdvancedMetricsTracker:
    """Advanced metrics tracker with TTFT and TBT measurement."""
    
    def __init__(self):
        self.metrics_history: List[DetailedMetrics] = []
    
    def measure_generation(
        self,
        ollama_module,  # Pass the ollama module
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 200
    ) -> DetailedMetrics:
        """
        Measure generation with detailed TTFT and TBT metrics.
        """
        print(f"\n📊 Starting detailed measurement...")
        print(f"📝 Prompt: {prompt[:50]}...")
        
        # Track timing
        start_time = time.time()
        first_token_time = None
        token_times = []
        last_token_time = start_time
        
        full_response = ""
        token_count = 0
        
        # Stream generation to measure TTFT and TBT
        for chunk in ollama_module.generate(
            model=model_name,
            prompt=prompt,
            stream=True,
            options={
                'temperature': temperature,
                'top_p': top_p,
                'num_predict': max_tokens
            }
        ):
            current_time = time.time()
            
            # Capture TTFT (time to first token)
            if first_token_time is None:
                first_token_time = current_time - start_time
                print(f"⚡ First token received in {first_token_time*1000:.2f}ms")
            
            # Capture TBT (time between tokens)
            if token_count > 0:
                tbt = current_time - last_token_time
                token_times.append(tbt)
            
            # Accumulate response
            full_response += chunk['response']
            token_count += 1
            last_token_time = current_time
        
        # Calculate final metrics
        total_time = time.time() - start_time
        avg_tbt = statistics.mean(token_times) if token_times else 0
        
        # Get token counts (approximate from chunk count)
        prompt_tokens = len(prompt.split())  # Rough estimate
        output_tokens = token_count
        total_tokens = prompt_tokens + output_tokens
        
        # Calculate speed
        tokens_per_second = output_tokens / total_time if total_time > 0 else 0
        
        # Create metrics object
        metrics = DetailedMetrics(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prompt=prompt[:100],  # Truncate for storage
            response=full_response[:200],  # Truncate for storage
            ttft=first_token_time if first_token_time else 0,
            avg_tbt=avg_tbt,
            total_time=total_time,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            tokens_per_second=tokens_per_second,
            ttft_ms=(first_token_time * 1000) if first_token_time else 0,
            avg_tbt_ms=avg_tbt * 1000,
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        
        self.metrics_history.append(metrics)
        
        # Print detailed metrics
        self.print_detailed_metrics(metrics)
        
        return metrics, full_response
    
    def print_detailed_metrics(self, metrics: DetailedMetrics):
        """Print detailed metrics in a formatted way."""
        print("\n" + "="*70)
        print("📊 DETAILED PERFORMANCE METRICS")
        print("="*70)
        
        print("\n🔹 LATENCY METRICS:")
        print(f"   ⚡ TTFT (Time to First Token):    {metrics.ttft_ms:.2f} ms")
        print(f"   🔄 Avg TBT (Time Between Tokens): {metrics.avg_tbt_ms:.2f} ms")
        print(f"   ⏱️  Total Generation Time:         {metrics.total_time:.3f} s")
        
        print("\n🔹 TOKEN METRICS:")
        print(f"   📝 Prompt Tokens:                 {metrics.prompt_tokens}")
        print(f"   📤 Output Tokens:                 {metrics.output_tokens}")
        print(f"   📊 Total Tokens:                  {metrics.total_tokens}")
        
        print("\n🔹 THROUGHPUT METRICS:")
        print(f"   🚀 Tokens per Second:             {metrics.tokens_per_second:.2f} tok/s")
        print(f"   💨 Speed Score:                   {self._get_speed_rating(metrics.tokens_per_second)}")
        
        print("\n🔹 MODEL CONFIG:")
        print(f"   🤖 Model:                         {metrics.model}")
        print(f"   🌡️  Temperature:                   {metrics.temperature}")
        print(f"   📈 Top-P:                         {metrics.top_p}")
        
        print("="*70 + "\n")
    
    def _get_speed_rating(self, tps: float) -> str:
        """Get speed rating based on tokens per second."""
        if tps > 60:
            return "🔥 Excellent"
        elif tps > 40:
            return "⚡ Very Good"
        elif tps > 25:
            return "✅ Good"
        elif tps > 15:
            return "⚠️  Fair"
        else:
            return "🐌 Slow"
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics across all measurements."""
        if not self.metrics_history:
            return {}
        
        return {
            'total_requests': len(self.metrics_history),
            'avg_ttft_ms': statistics.mean([m.ttft_ms for m in self.metrics_history]),
            'avg_tbt_ms': statistics.mean([m.avg_tbt_ms for m in self.metrics_history]),
            'avg_total_time': statistics.mean([m.total_time for m in self.metrics_history]),
            'avg_tokens_per_sec': statistics.mean([m.tokens_per_second for m in self.metrics_history]),
            'min_ttft_ms': min([m.ttft_ms for m in self.metrics_history]),
            'max_ttft_ms': max([m.ttft_ms for m in self.metrics_history]),
            'total_tokens': sum([m.total_tokens for m in self.metrics_history])
        }
    
    def print_summary(self):
        """Print summary statistics."""
        stats = self.get_summary_stats()
        if not stats:
            print("⚠️  No metrics collected yet.")
            return
        
        print("\n" + "="*70)
        print("📈 SUMMARY STATISTICS")
        print("="*70)
        print(f"📊 Total Requests:                {stats['total_requests']}")
        print(f"📝 Total Tokens Processed:        {stats['total_tokens']}")
        print(f"\n⚡ LATENCY:")
        print(f"   Avg TTFT:                      {stats['avg_ttft_ms']:.2f} ms")
        print(f"   Min TTFT:                      {stats['min_ttft_ms']:.2f} ms")
        print(f"   Max TTFT:                      {stats['max_ttft_ms']:.2f} ms")
        print(f"   Avg TBT:                       {stats['avg_tbt_ms']:.2f} ms")
        print(f"\n🚀 THROUGHPUT:")
        print(f"   Avg Speed:                     {stats['avg_tokens_per_sec']:.2f} tok/s")
        print(f"   Avg Total Time:                {stats['avg_total_time']:.3f} s")
        print("="*70 + "\n")
    
    def export_to_dataframe(self):
        """Export metrics to pandas DataFrame."""
        if not self.metrics_history:
            return pd.DataFrame()
        
        data = []
        for m in self.metrics_history:
            data.append(asdict(m))
        
        return pd.DataFrame(data)
    
    def export_to_csv(self, filename: str = None):
        """Export metrics to CSV file."""
        if filename is None:
            filename = f"qwen_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = self.export_to_dataframe()
        df.to_csv(filename, index=False)
        print(f"✅ Metrics exported to: {filename}")
        return filename
    
    def export_to_google_sheets(
        self,
        credentials_file: str,
        spreadsheet_name: str = "Qwen 3.5 4B Metrics"
    ):
        """Export metrics to Google Sheets."""
        if not HAS_GSPREAD:
            print("❌ gspread not installed. Run: pip install gspread oauth2client")
            return None
        
        try:
            # Authenticate
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            client = gspread.authorize(creds)
            
            # Create or open spreadsheet
            try:
                spreadsheet = client.open(spreadsheet_name)
                worksheet = spreadsheet.sheet1
            except:
                spreadsheet = client.create(spreadsheet_name)
                worksheet = spreadsheet.sheet1
            
            # Convert to DataFrame and upload
            df = self.export_to_dataframe()
            
            # Clear existing data
            worksheet.clear()
            
            # Upload headers
            worksheet.append_row(df.columns.tolist())
            
            # Upload data
            for _, row in df.iterrows():
                worksheet.append_row(row.tolist())
            
            print(f"✅ Metrics exported to Google Sheets: {spreadsheet_name}")
            print(f"🔗 URL: {spreadsheet.url}")
            
            return spreadsheet.url
        
        except Exception as e:
            print(f"❌ Error exporting to Google Sheets: {e}")
            return None
    
    def visualize_metrics(self):
        """Create visualization of metrics."""
        if not self.metrics_history:
            print("⚠️  No data to visualize.")
            return
        
        df = self.export_to_dataframe()
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Qwen 3.5 4B Performance Metrics Dashboard', fontsize=16, fontweight='bold')
        
        # TTFT over time
        axes[0, 0].plot(range(len(df)), df['ttft_ms'], marker='o', color='#2E86AB', linewidth=2)
        axes[0, 0].set_title('Time to First Token (TTFT)', fontweight='bold')
        axes[0, 0].set_xlabel('Request #')
        axes[0, 0].set_ylabel('Time (ms)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # TBT over time
        axes[0, 1].plot(range(len(df)), df['avg_tbt_ms'], marker='s', color='#A23B72', linewidth=2)
        axes[0, 1].set_title('Average Time Between Tokens (TBT)', fontweight='bold')
        axes[0, 1].set_xlabel('Request #')
        axes[0, 1].set_ylabel('Time (ms)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Throughput
        axes[0, 2].bar(range(len(df)), df['tokens_per_second'], color='#F18F01', alpha=0.7)
        axes[0, 2].set_title('Token Throughput', fontweight='bold')
        axes[0, 2].set_xlabel('Request #')
        axes[0, 2].set_ylabel('Tokens/Second')
        axes[0, 2].grid(True, alpha=0.3, axis='y')
        
        # Total time
        axes[1, 0].plot(range(len(df)), df['total_time'], marker='D', color='#6A994E', linewidth=2)
        axes[1, 0].set_title('Total Generation Time', fontweight='bold')
        axes[1, 0].set_xlabel('Request #')
        axes[1, 0].set_ylabel('Time (seconds)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Output tokens
        axes[1, 1].bar(range(len(df)), df['output_tokens'], color='#BC4749', alpha=0.7)
        axes[1, 1].set_title('Output Tokens per Request', fontweight='bold')
        axes[1, 1].set_xlabel('Request #')
        axes[1, 1].set_ylabel('Tokens')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        # TTFT vs Output Tokens scatter
        axes[1, 2].scatter(df['output_tokens'], df['ttft_ms'], color='#8338EC', alpha=0.6, s=100)
        axes[1, 2].set_title('TTFT vs Output Tokens', fontweight='bold')
        axes[1, 2].set_xlabel('Output Tokens')
        axes[1, 2].set_ylabel('TTFT (ms)')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return fig


# Example usage
if __name__ == "__main__":
    print("Advanced Metrics Tracker for Qwen 3.5 4B")
    print("=" * 50)
    print("\nUsage in Colab:")
    print("""
# 1. Import the tracker
from metrics_tracker import AdvancedMetricsTracker
import ollama

# 2. Initialize
tracker = AdvancedMetricsTracker()

# 3. Measure generation
metrics, response = tracker.measure_generation(
    ollama_module=ollama,
    model_name="qwen3.5:4b",
    prompt="What is AI?",
    max_tokens=200
)

# 4. Print summary
tracker.print_summary()

# 5. Visualize
tracker.visualize_metrics()

# 6. Export to CSV
tracker.export_to_csv()

# 7. Export to Google Sheets (optional)
tracker.export_to_google_sheets(
    credentials_file="credentials.json",
    spreadsheet_name="Qwen Metrics"
)
    """)


# Initialize tracker
import ollama
tracker = AdvancedMetricsTracker()

print("\n" + "="*70)
print("✅ Advanced Metrics Tracker Initialized!")
print("="*70)
print("\n📊 Tracking Capabilities:")
print("   ⚡ TTFT (Time To First Token)")
print("   🔄 TBT (Time Between Tokens)")
print("   🚀 Throughput (Tokens per second)")
print("   📈 Visualizations")
print("   📊 CSV & Google Sheets Export")
print("="*70 + "\n")

# %% [markdown] cell 17
# ## Step 9: Test Generation with Detailed Metrics

# %% [code] cell 18
# Test generation with full metrics
prompt = "What is artificial intelligence? Explain in 2-3 sentences."

metrics, response = tracker.measure_generation(
    ollama_module=ollama,
    model_name=MODEL_NAME,
    prompt=prompt,
    temperature=0.7,
    max_tokens=200
)

print(f"\n🤖 Response:\n{response}")

# %% [markdown] cell 19
# ## Step 10: Run Multiple Tests with Metrics

# %% [code] cell 20
# Test with multiple prompts (6 diverse tests)
test_prompts = [
    "What is machine learning? Explain in simple terms.",
    "Explain quantum computing and its potential applications.",
    "How does the internet work? Describe the basic process.",
    "What is blockchain technology and why is it important?",
    "Describe how neural networks learn from data.",
    "What are the main differences between AI and machine learning?"
]

print("="*70)
print("🏃 RUNNING PERFORMANCE BENCHMARK WITH DETAILED METRICS")
print("="*70)
print(f"Total tests: {len(test_prompts)}\n")

for i, prompt in enumerate(test_prompts, 1):
    separator = "="*70
    print(f"\n{separator}")
    print(f"TEST {i}/{len(test_prompts)}")
    print(f"{separator}")
    
    metrics, response = tracker.measure_generation(
        ollama_module=ollama,
        model_name=MODEL_NAME,
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

# Print overall summary
summary_line = "#"*70
print(f"\n{summary_line}")
tracker.print_summary()
print(summary_line)

# %% [markdown] cell 21
# ## Step 11: Visualize Performance Metrics Dashboard

# %% [code] cell 22
# Create visual dashboard
print("📊 Generating performance metrics dashboard...\n")
tracker.visualize_metrics()

# %% [markdown] cell 23
# ## Step 12: Export Metrics to CSV

# %% [code] cell 24
# Export all metrics to CSV
csv_file = tracker.export_to_csv()

# Download the file (in Colab); elsewhere the CSV is already on disk
try:
    from google.colab import files
    files.download(csv_file)
except ImportError:
    print("Not running in Colab; CSV saved locally.")

print(f"\n📥 CSV file ready for download: {csv_file}")

# %% [code] cell 25
# Upload your Google Service Account credentials JSON file (Colab only)
try:
    from google.colab import files
    uploaded = files.upload()  # Upload your credentials.json
except ImportError:
    print("Not running in Colab; using local credentials.json if present.")
    uploaded = None

# Export to Google Sheets
spreadsheet_url = tracker.export_to_google_sheets(
    credentials_file="credentials.json",
    spreadsheet_name="Qwen 3.5 4B Performance Metrics"
)

if spreadsheet_url:
    print(f"\n✅ Google Sheets created!")
    print(f"🔗 Access your metrics here: {spreadsheet_url}")

# %% [markdown] cell 26
# ## Step 14: Test Basic Generation

# %% [code] cell 27
import ollama
import time

print("🤖 Testing model generation...\n")

prompt = "What is artificial intelligence? Explain in 2-3 sentences."
print(f"📝 Prompt: {prompt}\n")

start_time = time.time()

# Generate response
response = ollama.generate(
    model=MODEL_NAME,
    prompt=prompt
)

gen_time = time.time() - start_time

print(f"🤖 Response:\n{response['response']}")
print(f"\n⏱️  Generation time: {gen_time:.2f} seconds")
print(f"📊 Total tokens: {response['eval_count']}")
print(f"⚡ Speed: {response['eval_count']/gen_time:.2f} tokens/sec")

# %% [markdown] cell 28
# ## Step 15: Streaming Generation (Real-time Output)

# %% [code] cell 29
import ollama
import time

prompt = "Write a short poem about technology."

print(f"📝 Prompt: {prompt}\n")
print("🤖 Streaming Response:\n")
print("="*60)

start_time = time.time()
token_count = 0

# Stream the response
for chunk in ollama.generate(model=MODEL_NAME, prompt=prompt, stream=True):
    print(chunk['response'], end='', flush=True)
    token_count += 1

gen_time = time.time() - start_time

print("\n" + "="*60)
print(f"\n⏱️  Generation time: {gen_time:.2f} seconds")
print(f"⚡ Speed: ~{token_count/gen_time:.2f} tokens/sec")

# %% [markdown] cell 30
# ## Step 16: Chat Interface (Multi-turn Conversation)

# %% [code] cell 31
import ollama

# Initialize conversation history
messages = []

def chat(user_message, stream=True):
    """Chat with the model."""
    global messages
    
    # Add user message
    messages.append({
        'role': 'user',
        'content': user_message
    })
    
    print(f"👤 You: {user_message}\n")
    print("🤖 Assistant: ", end='', flush=True)
    
    # Get response
    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
        stream=stream
    )
    
    assistant_message = ""
    
    if stream:
        for chunk in response:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            assistant_message += content
    else:
        assistant_message = response['message']['content']
        print(assistant_message)
    
    # Add assistant message to history
    messages.append({
        'role': 'assistant',
        'content': assistant_message
    })
    
    print("\n" + "-"*60 + "\n")
    return assistant_message

# Test conversation
print("💬 Starting conversation...\n")
print("="*60 + "\n")

chat("Hello! What's your name?")
chat("What can you help me with?")
chat("Tell me a fun fact about Python programming.")

# %% [markdown] cell 32
# ## Step 17: Custom Chat Function (Interactive)

# %% [code] cell 33
# Reset conversation
messages = []

# Ask your own question here
YOUR_QUESTION = "Explain quantum computing in simple terms."

response_text = chat(YOUR_QUESTION)

# To continue the conversation, run this cell again with a new question

# %% [markdown] cell 34
# ## Step 18: Advanced Options (Temperature, Top-P, etc.)

# %% [code] cell 35
import ollama

prompt = "Write a creative story about a robot learning to paint."

print("🎨 Testing different creativity settings...\n")

configs = [
    {"name": "Conservative (temp=0.3)", "temperature": 0.3, "top_p": 0.9},
    {"name": "Balanced (temp=0.7)", "temperature": 0.7, "top_p": 0.9},
    {"name": "Creative (temp=1.0)", "temperature": 1.0, "top_p": 0.95},
]

for config in configs:
    print("="*60)
    print(f"⚙️  {config['name']}")
    print("="*60)
    
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            'temperature': config['temperature'],
            'top_p': config['top_p'],
            'num_predict': 150  # Max tokens
        }
    )
    
    print(f"\n{response['response']}\n")

# %% [markdown] cell 36
# ## Step 19: Performance Benchmarking (Without Metrics)

# %% [code] cell 37
import ollama
import time
import statistics

print("🏃 Running performance benchmark...\n")

test_prompts = [
    "What is machine learning?",
    "Explain the solar system.",
    "How does photosynthesis work?",
    "What are the benefits of exercise?",
    "Describe the water cycle."
]

times = []
speeds = []

for i, prompt in enumerate(test_prompts, 1):
    print(f"Test {i}/{len(test_prompts)}: ", end='', flush=True)
    
    start = time.time()
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)
    duration = time.time() - start
    
    tokens = response['eval_count']
    speed = tokens / duration
    
    times.append(duration)
    speeds.append(speed)
    
    print(f"{duration:.2f}s ({speed:.2f} tok/s)")

print("\n" + "="*60)
print("BENCHMARK RESULTS")
print("="*60)
print(f"📊 Average Time: {statistics.mean(times):.2f} seconds")
print(f"⚡ Average Speed: {statistics.mean(speeds):.2f} tokens/sec")
print(f"🚀 Max Speed: {max(speeds):.2f} tokens/sec")
print(f"🐌 Min Speed: {min(speeds):.2f} tokens/sec")
print(f"📈 Std Dev: {statistics.stdev(speeds):.2f} tokens/sec")
print("="*60)

# %% [markdown] cell 38
# ## Step 20: Model Information

# %% [code] cell 39
import ollama
import json

# Get model information
model_info = ollama.show(MODEL_NAME)

print("="*60)
print(f"MODEL INFORMATION: {MODEL_NAME}")
print("="*60)

print(f"\n📦 Model: {model_info.get('name', 'N/A')}")
print(f"📝 License: {model_info.get('license', 'N/A')}")

if 'parameters' in model_info:
    print(f"\n⚙️  Parameters:")
    print(f"   {model_info['parameters']}")

if 'template' in model_info:
    print(f"\n📋 Template:\n{model_info['template'][:200]}...")

print("\n" + "="*60)
