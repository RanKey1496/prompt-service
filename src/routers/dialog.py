from fastapi import APIRouter
from services.dialog_service import generate_random_dialog, generate_script

router = APIRouter()

@router.get("/dialogs/random")
def get_random_dialog(category: str) -> dict:
    return generate_random_dialog(category)

@router.get("/dialogs/script")
def get_script_from_text(text: str) -> dict:
    return generate_script(text)