"""
Unified Runner for Backend and Frontend
Run both API server and Streamlit frontend
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_backend():
    """Run FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
        cwd=Path(__file__).parent
    )

def run_frontend():
    """Run Streamlit frontend with auto-reload enabled"""
    print("🎨 Starting Streamlit frontend...")
    print("   📝 Auto-reload enabled - แก้โค้ดแล้วจะอัพเดทอัตโนมัติ!")
    time.sleep(3)  # Wait for backend to start
    
    # Set environment variable to skip email prompt
    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    return subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "frontend.py",
            "--server.port", "8501",
            "--server.runOnSave", "true",
            "--server.fileWatcherType", "auto",
            "--browser.gatherUsageStats", "false",
            "--client.showErrorDetails", "true",
            "--runner.fastReruns", "true"
        ],
        cwd=Path(__file__).parent,
        env=env
    )

def main():
    """Run both backend and frontend"""
    print("=" * 60)
    print("🚀 FastAPI Summarize - Starting Application")
    print("=" * 60)
    print()
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = run_backend()
        
        # Start frontend
        frontend_process = run_frontend()
        
        print()
        print("=" * 60)
        print("✅ Application started successfully!")
        print("=" * 60)
        print()
        print("📍 Access Points:")
        print("   • Frontend UI:  http://localhost:8501")
        print("   • API Docs:     http://localhost:8000/docs")
        print("   • API ReDoc:    http://localhost:8000/redoc")
        print()
        print("💡 Tips:")
        print("   • Frontend จะเปิดใน 5-10 วินาที")
        print("   • ✨ Auto-reload enabled - แก้โค้ดจะอัพเดทอัตโนมัติ!")
        print("   • แก้ไข frontend.py หรือ app/* แล้วเห็นผลทันที")
        print()
        print("⏹️  Press Ctrl+C to stop all services")
        print("=" * 60)
        print()
        
        # Wait for processes
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        
        if backend_process:
            backend_process.terminate()
            print("   ✓ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("   ✓ Frontend stopped")
        
        print("\n👋 Goodbye!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
