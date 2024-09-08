# Sistema de Agendamento de Barbearia

Este é um sistema de agendamento de barbearia desenvolvido em Django, que permite que os clientes agendem serviços, escolham horários disponíveis e acompanhem o andamento de seus agendamentos. 

## Funcionalidades

- **Gerenciamento de Agendamentos**: Os clientes podem agendar serviços, visualizar horários disponíveis e cancelar agendamentos.
- **Atualização de Status de Atendimento**: Diferenciação entre clientes e barbeiros, permitindo que os barbeiros finalize o status dos atendimentos.
- **Relatórios**: Visualização de lucro que a barbearia obteve no mês, e quantidade de atendimento por barbeiro.
- **Sistema de Usuários**: Diferenciação entre clientes, barbeiros e gerentes.
- **Painel Administrativo**: Gerenciamento de usuários e relatórios.

## Requisitos

- Python 3.12.6
- Django 5.0.6
- PostgreSQL (opcional)
- Jazzmin (tema para o Django Admin)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/sistema-agendamento-barbearia.git

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

3. Instale as dependências:
   ````bash
     pip install -r requirements.txt

4. Aplique as migrações:
   ````bash
     python manage.py migrate

5. Crie um superusuário para acessar o painel administrativo:
   ````bash
     python manage.py createsuperuser

5. Inicie o servidor de desenvolvimento:
   ````bash
     python manage.py runserver

# Algumas imagens do Projeto

# Landing Page
![image](https://github.com/user-attachments/assets/01c0498c-8f70-4cc2-9913-5274133b8776)

![image](https://github.com/user-attachments/assets/6e288049-9605-4843-9962-17ee6bac9784)

![image](https://github.com/user-attachments/assets/a522537f-0ee4-4b93-8975-d788eeaeb609)

Ao passar o mouse sobre a imagem ela expande para frente
![image](https://github.com/user-attachments/assets/8e746d51-737d-444b-b8a5-25cb2b676846)

# Sistema

# Área do cliente

**Agendar horário** - 
cliente consegue ver quais os profissionais estão com horários em aberto
![image](https://github.com/user-attachments/assets/eec88f3d-8917-4db9-bb26-3d5987d83315)

**Ver Agendamentos e detalhes do agendamento** -
Cliente ver seus agendamentos e ao clicar em detalhes ver o detalhamento do agendamento
![image](https://github.com/user-attachments/assets/a556cae6-69b4-4a50-9d57-2767dfcfbf57)

**Detalhe do agendamento**
![image](https://github.com/user-attachments/assets/9b7c2f37-9e4f-46df-a87d-4e177d1fc45d)

**Cancelamento do agendamento** -
Cliente pode cancelar seu agendamento, status é atualizado automaticamente
![image](https://github.com/user-attachments/assets/923d6daf-b80a-487d-be71-f62e4f814473)

# Área do barbeiro

**Abrir horário** -
Barbeiro pode abrir os horários disponíveis
![image](https://github.com/user-attachments/assets/ba2be9f7-2a9d-43a6-bb5c-8868ae9f36cf)

**Ver agendamentos**
Barbeiro pode ver os agendamentos que os cliente agendou com ele, tanto os da data atual como as datas futuras
![image](https://github.com/user-attachments/assets/e7c238e5-4b8f-4004-82b9-15e56b0c6b1f)

**Detalhes do agendamento**
Assim como o cliente pode cancelar um agendamento, o barbeiro pode finalizar o atendimento, essa etapa é muito importante, pois é através da finalização do atendimento que é o relatório mensal de lucro é feito
![image](https://github.com/user-attachments/assets/dffca4b2-3564-4988-8add-e8c8a64bb53d)
