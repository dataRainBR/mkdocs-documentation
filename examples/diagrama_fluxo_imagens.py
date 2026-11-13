import base64
from pathlib import Path

import drawpyo


project_root = Path(__file__).resolve().parents[1]
assets_dir = project_root / "docs" / "assets"
output_dir = assets_dir / "diagrams"
output_dir.mkdir(parents=True, exist_ok=True)

diagram = drawpyo.File()
diagram.file_path = str(output_dir.resolve())
diagram.file_name = "fluxo-imagens.drawio"

page = drawpyo.Page(file=diagram)
page.name = "Usuário até S3"

etapas = [
    ("user.png", "Usuário"),
    ("imagem1.png", "Imagem 1"),
    ("Api_gateway.png", "API Gateway"),
    ("lambda.png", "Lambda"),
    ("s3.png", "S3"),
]

icones = []
posicao_inicial_x = 55
distancia_entre_etapas = 170
posicao_y = 120

for indice, (nome_arquivo, rotulo) in enumerate(etapas):
    caminho_imagem = assets_dir / nome_arquivo
    if not caminho_imagem.is_file():
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")

    imagem_base64 = base64.b64encode(caminho_imagem.read_bytes()).decode("ascii")
    x = posicao_inicial_x + indice * distancia_entre_etapas

    icone = drawpyo.diagram.Object(page=page, value="")
    icone.position = (x, posicao_y)
    icone.width = 72
    icone.height = 72
    icone.apply_style_string(
        "shape=image;"
        "aspect=fixed;"
        "imageAspect=0;"
        f"image=data:image/png;base64,{imagem_base64};"
    )
    icones.append(icone)

    legenda = drawpyo.diagram.Object(
        page=page,
        value=rotulo,
        position=(x - 30, posicao_y + 82),
        width=132,
        height=32,
    )
    legenda.text_format.align = "center"
    legenda.fillColor = "none"
    legenda.strokeColor = "none"

for origem, destino in zip(icones, icones[1:]):
    conexao = drawpyo.diagram.Edge(page=page, source=origem, target=destino)
    conexao.strokeColor = "#526B7A"
    conexao.strokeWidth = 2
    conexao.apply_style_string("endArrow=block;")

diagram.write()
print(f"Diagrama salvo em: {output_dir / diagram.file_name}")
