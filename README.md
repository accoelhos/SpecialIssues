## Sistema de Consulta de Special Issues
Esse projeto tem como objetivo desenvolver (em python, com auxilio da biblioteca flask) um website que armazena Special Issues de diferentes revistas de artigos na área de ciência da computação. 
Além de armazenar, o site mostra as Special Issues disponíveis e permite que um admin. insira novas chamadas.

- O site está disponível em https://rukbat.eic.cefet-rj.br/special/
  
## Como rodar o projeto
- Após clonar o repositório, abrir um terminal:
- Entrar na pasta do projeto:
```
cd SpecialIssues
```
- Instalar o ambiente virtual
```
pip install virtualenv
python -m virtualenv myvenv
myvenv\Scripts\Activate (Windows)
source myvenv/bin/activate (Linux ou macOS) 
```
- Instalar as dependências do projeto
```
pip install -r requirements.txt
```
- Executar o app
```
python app.py
```
