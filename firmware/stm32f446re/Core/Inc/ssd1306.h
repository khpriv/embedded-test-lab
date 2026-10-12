#ifndef SSD1306_H
#define SSD1306_H

#include "stm32f4xx_hal.h"

void SSD1306_Init(I2C_HandleTypeDef *hi2c);
void SSD1306_AllPixelsOn(void);
void SSD1306_AllPixelsOff(void);

void SSD1306_Clear(void);
void SSD1306_DrawPixel(
    uint8_t x,
    uint8_t y,
    uint8_t on
);
void SSD1306_UpdateScreen(void);

void SSD1306_SetCursor(uint8_t, uint8_t);
void SSD1306_WriteString(const char *);

#endif
