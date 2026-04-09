from fastapi import APIRouter
import subprocess
import sys
import os

router = APIRouter()

@router.post("/run")
def run_analysis():
    """
    Run full analysis pipeline by executing the script
    """

    script_path = os.path.join("scripts", "run_full_analysis.py")

    try:
        subprocess.run([sys.executable, script_path], check=True)
        return {"message": "Analysis pipeline completed successfully"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}