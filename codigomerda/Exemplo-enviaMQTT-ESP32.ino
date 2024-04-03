// Exemplo de envio de informação via MQTT pelo ESP32
#include <PubSubClient.h>
#include <WiFi.h>

// Conexão com o WiFI
const char *SSID = "VISITANTES";
const char *PWD = "";

// configurações de conexão MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
char *mqttServer = "broker.hivemq.com";
int mqttPort = 1883;

// função para conectar ao WiFi
void ConectaNoWiFi() {
    Serial.print("Conectando ao WiFi");
    WiFi.begin(SSID, PWD);
    // Caso tenha dificuldades em conectar, imprime um “.”
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    // Se conectado, imprime “Conectado”
    Serial.print("Conectado.");
}

// Realiza as configurações do MQTT
void setupMQTT() { mqttClient.setServer(mqttServer, mqttPort); }

// Realiza a conceção com o Broker MQTT
void conectaBrokerMQTT() {
    Serial.println("Conectando ao broker");
    // A função mqttClient.connected() verifica se existe uma conexão ativa.
    // Depende do Broker, a conexão pode se manter ativa, ou desativar a cada
    // envio de msg.
    while (!mqttClient.connected()) {
        // Se entrou aqui, é porque não está conectado. Então será feito uma
        // tentativa de conexão infinita, até ser conectado.
        Serial.println("Conectando ao Broker MQTT");
        // define o nome da ESP na conexão. Está sendo gerado um nome aleatório,
        // para evitar ter duas ESPs com o mesmo nome. Neste caso, uma
        // derrubaria a outra.
        String clientId = "ESP32Client-";
        clientId += String(random(0xffff), HEX);
        // Realiza a conexão com a função “mqttClient.connect”. Caso seja um
        // sucesso, entra no if e imprime “Conectado ao Broker MQTT.”
        if (mqttClient.connect(clientId.c_str())) {
            Serial.println("Conectado ao Broker MQTT.");
        }
    }
}

// setup
void setup() {
    Serial.begin(9600);
    ConectaNoWiFi();
    setupMQTT();
}

// loop
void loop() {
    // Verifica se a conexão está ativa, caso não esteja, tenta conectar
    // novamente.
    if (!mqttClient.connected()) {
        conectaBrokerMQTT();
    }
    // Publica no tópico “/NomeDoTopico” a msg “ola mundo”
    mqttClient.publish("/NomeDoTopico", "ola mundo!");
    // Caso você tenha que enviar outra informação, que não seja texto, como
    // int, float, entre outros, é preciso converter para texto (String/char[]).
    // Uma opção é a utilização da função “sprintf”. As próximas linhas
    // convertem um float em texto, e então envia para o tópico
    // “/NomeDoSegundoTopico”.
    char data[10];
    float num = 10;
    sprintf(data, "%f", num);
    mqttClient.publish("/NomeDoSegundoTopico", data);
    Serial.println("Mensagem enviada!");
    // realiza o sincronismo com o Broker, por exemplo, verifica se existem msgs
    // para ler se estiver inscrito em algum tópico
    mqttClient.loop();
    // Aguarda 1 segundo, para que não fique enviando msgs sem parar a um
    // intervalo de tempo muito curto.
    delay(1000);
}