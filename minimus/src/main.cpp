#include "esp32-hal-gpio.h"
#include "hal/gpio_types.h"
#include <Arduino.h>
#include <array>

constexpr std::array<int, 3> password_order{ 1, 0, 2 };
constexpr std::array<gpio_num_t, 3> buttons{ GPIO_NUM_27, GPIO_NUM_26, GPIO_NUM_25 };

void setup() {
    Serial.begin(115200);
    for (auto i : buttons)
        pinMode(i, INPUT_PULLUP);

    pinMode(GPIO_NUM_14, OUTPUT);
    pinMode(GPIO_NUM_35, INPUT_PULLUP);

    // tone(GPIO_NUM_14, 1000);
}

void loop() {
    static auto tick = 0;

    if (millis() - tick >= 1000) {
        Serial.print("Botões: ");
        for (auto b : buttons)
            Serial.printf("%d ", digitalRead(b));

        Serial.print("\n");

        Serial.println(digitalRead(GPIO_NUM_35));

        tick = millis();
    }
}
