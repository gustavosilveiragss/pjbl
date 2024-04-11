#include <Arduino.h>
#include <array>
#include "Button.hpp"
#include "esp32-hal-gpio.h"

void setup() {
    Serial.begin(115200);

    pinMode(GPIO_NUM_14, OUTPUT);
    pinMode(GPIO_NUM_35, INPUT);
}

void loop() {
    std::array buttons{ Button{ GPIO_NUM_27 }, Button{ GPIO_NUM_26 }, Button{ GPIO_NUM_25 } };

    std::array password{ 1, 0, 2 };
    std::vector<size_t> password_attempt;
    bool got_correct_password = false;
    bool is_lid_open = false;

    while (true) {
        if (not got_correct_password) {
            for (size_t i = 0; i < buttons.size(); ++i) {
                if (buttons[i].is_clicked()) {
                    Serial.printf("Button %d clicked\n", i);
                    password_attempt.push_back(i);

                    if (password_attempt.size() == password.size()) {
                        got_correct_password = std::equal(password_attempt.begin(), password_attempt.end(), password.begin());
                        Serial.println(got_correct_password ? "Correct password!" : "Wrong password!");
                        password_attempt.clear();
                        break;
                    }
                }
            }
        }

        const auto old_is_lid_open = std::exchange(is_lid_open, digitalRead(GPIO_NUM_35));
        if (is_lid_open != old_is_lid_open) {
            if (is_lid_open) {
                Serial.println("Lid opened!");
                if (not got_correct_password) {
                    Serial.println("Alarm!");
                } else {
                    Serial.println("Lid opened but no alarm!");
                }
            } else {
                got_correct_password = false;
                Serial.println("Lid closed!");
            }
        }
    }
}
