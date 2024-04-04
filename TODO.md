# TODO

* [ ] relatorio hardware
  * [ ] detalhar cada modulo
* [ ] relatório software/firmware
  * [ ] "explicação detalhada da função de cada código" - acho q seria só detalhar o q cada arquivo faz no geral
  * [ ] Explicar o que cada tópico do mqtt faz
  * [ ] Explicar responsabilidade firmware/python/node-red
* [ ] Implementar firmware enviando tópicos mqtt
  * [ ] Implementar detecção senha
    * [ ] salva em flash
    * [ ] envia tópico informando que deu boa/ruim
    * [ ] se deu certo -> muda para estado de permitir abertura
  * [ ] Implementar detecção abertura
    * [ ] Implementar infravermelho
      * [ ] caso receptor saia de contato com emissor, muda para estado de aberto
      * [ ] com delay, envia tópico do estado de aberto/fechado
    * [ ] Caso estado de aberto e não permite abertura (não deu senha certa) -> liga buzzer
      * [ ] frequência a partir do que está salvo
      * [ ] Envia tópico q tentaram invadir
* [ ] Implementar python recebendo/enviando mqtt
  * [ ] Implementar mudança de senha
  * [ ] Implementar mudança de frequencia
* [ ] Implementar dashboard node-red
  * [ ] Display se está permitindo ou não abertura
  * [ ] Display se está ou não aberto
  * [ ] Display senha atual
    * [ ] Campo de input -> envia tópico de alteração ao python
  * [ ] Display frequência atual
    * [ ] Campo de input -> envia tópico de alteração ao python
* [ ] Gravar o vídeo