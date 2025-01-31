import g4f
import re
from fastapi import HTTPException

def generate_llm_response(prompt: str) -> str:
    return g4f.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    
def random_dialog(category: str) -> str:
    prompt = f"""
    Genera un titulo de un tema alteatorio SOBRE MOTOS y/o MARCAS DE MOTOS dependiendo de la categoria que no supere 10 palabras, dependiendo del tema.
    El titulo debe ser retornado como un string con un numero especifico de palabras.
    Aquí hay un ejemplo del string:
    "Ducati lider en tecnología durante años"
    Vaya directo al grano, no empiece con cosas innecesarias como "bienvenido este es el tema"
    NO DEBES EXCEDER LAS 10 PALABRAS.
    NO DEBES INCLUIR NINGUN TIPO DE MARCA O FORMATO EN EL TEXTO.
    DEBES ESCRIBIR EL TEXTO EN ESPAÑOL
    SOLO RETORNA EL CONTENIDO CRUDO DEL TEXTO. NO INCLUYAS "VOICEOVER", "NARRATOR" O INDICADORES SIMILARES DE QUE DEBERIA DECIRSE AL INICIO DEL TEXTO O TEMA.
    NO DEBES MENCIONAR EL PROMPT O ALGUNA COSA SOBRE EL TEXTO EN SI. ADEMAS, NO HABLES SOBRE LA CANTIDAD DE PALABRAS. SOLO ESCRIBE EL TITULO.
    
    Categoria: {category}
    """
    
    try_number = 0
    while try_number < 3:
        completion = generate_llm_response(prompt)
        completion = re.sub(r'[\*"]', '', completion)
        
        if not completion:
            print("El texto generado está vacío")
            try_number += 1
            continue
        
        if len(completion.split(' ')) > 10:
            print("El texto es demasiado largo")
            try_number += 1
            continue

        return { 'data': completion }
    raise Exception('No se pudo generar el texto luego de 3 intentos')

def script_from_text(text) -> str:
    prompt = f"""
    Genera un guion para un video en 4 oraciones, dependiendo en el titulo del video.
    El guion debe ser retornado como un string con un numero especifico de parrafos.
    Aquí hay un ejemplo del string:
    "Esto es un ejemplo de string."
    Bajo ninguna circunstancia haga referencia a esta solicitud en su respuesta.
    Vaya directo al grano, no empiece con cosas innecesarias como "bienvenido a este video".
    Obviamente, el guión debe estar relacionado con el tema del video.
    
    NO DEBE EXCEDER EL LÍMITE DE 4 ORACIONES. ASEGÚRESE DE QUE LAS 4 ORACIONES SEAN CORTAS.
    NO DEBE INCLUIR NINGÚN TIPO DE MARKDOWN O FORMATO EN EL GUIÓN, NUNCA UTILICE UN TÍTULO.
    DEBE ESCRIBIR EL GUIÓN EN EL IDIOMA ESPAÑOL.
    SOLO DEVUELVA EL CONTENIDO BRUTO DEL GUIÓN.
    NO INCLUYA "VOICEOVER", "NARRATOR" O INDICADORES SIMILARES DE LO QUE DEBE HABLARSE AL COMIENZO DE CADA PÁRRAFO O LÍNEA.
    NO DEBE MENCIONAR LA INSTRUCCIÓN NI NADA SOBRE EL GUIÓN EN SÍ.
    ADEMÁS, NUNCA HABLES DE LA CANTIDAD DE PÁRRAFOS O LÍNEAS.
    SOLO ESCRIBE EL GUIÓN.
    
    Titulo: {text}
    """
    
    try_number = 0
    while try_number < 3:
        completion = generate_llm_response(prompt)
        completion = re.sub(r'[\*"]', '', completion)
        
        if not completion:
            print("El texto generado está vacío")
            try_number += 1
            continue
        
        if len(completion) > 5000:
            print("El script generado es demasiado largo")
            try_number += 1
            continue
        
        return { 'data': completion }
    raise Exception('No se pudo generar el script luego de 3 intentos')
        

def generate_random_dialog(category: str):
    try:
        return random_dialog(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
def generate_script(text: str):
    try:
        return script_from_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)