
    Deverá ser uma continuação da aplicação Web apresentada no PJBL2.
    Deve ser utilizado o SQL Alchemy para realizar a interação com o banco de dados MySQL.
    A aplicação deve conter:
        Flask Login com autenticação de seção para todas as páginas.
        Classificação de usuário com Flask Role ou condições com pelo menos 3 tipos diferentes de usuário com operações distintas: Admin, Estatístico, Operador.
        Usuário admin poderá:
            Cadastrar usuários;
            Cadastrar kits;
            Editar usuários;
            Editar kits;
            Deletar Usuários;
            Deletar kits;
        Usuário Admin/Estatístico poderá:
            Visualizar dados em tempo real vindo do MQTT broker;
            Acesso a tela com dados históricos dos sensores;
        Usuário Admin/Operador:
            Acesso a tela de comandos remotos;
            Acesso a tela de dados históricos de atuações remotas;
        Usuário Admin/Estatístico/Operador:
            Pode fazer o logout do sistema.

 A entrega será realizada da seguinte forma:

    Um aluno do grupo deverá subir o sistema em forma de zip no AVA, e indicar no corpo da entrega o nome de todos os integrantes do grupo.
    Cada integrante do grupo deverá inserir no corpo da entrega o número do grupo e o nome de todos os integrantes.
    Deverão gravar um vídeo de no máximo 5 minutos explicando o funcionamento do sistema, e demonstrando todos os itens demandados.
    No caso da falta dos itens, pontos serão descontados. 
    É indispensável que todos os integrantes do grupo realizem a apresentação. Caso alguém do grupo não apresente, o mesmo não receberá nota.
    Após a revisão por parte dos professores, há a possibilidade de uma explicação por parte dos alunos em caso de dúvidas.
