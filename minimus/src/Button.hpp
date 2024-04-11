#pragma once

#include <Arduino.h>

class Button {
public:
    explicit Button(gpio_num_t io)
        : m_io(io) {
        pinMode(m_io, INPUT_PULLUP);
    }

    bool is_clicked() {
        if (millis() - m_last_update < DEBOUNCE_TIME)
            return false;

        m_last_update = millis();

        const auto last_state = std::exchange(m_state, digitalRead(m_io));
        return not m_state and last_state;
    }

private:
    bool m_state{ false };
    gpio_num_t m_io;

    uint32_t m_last_update{ 0 };

    // In milliseconds
    static constexpr auto DEBOUNCE_TIME = 100;
};
