#include <Arduino.h>

int d0 [] = { 5, 6, 7, 8, 11, 10 };
int d1 [] = { 5, 6 };
int d2 [] = { 7, 6, 9, 11, 10};
int d3 [] = { 7, 6, 5, 9, 10 };
int d4 [] = { 8, 9, 6, 5 };
int d5 [] = { 7, 8, 9, 5, 10 };
int d6 [] = { 7, 8, 9, 11, 10, 5 };
int d7 [] = { 7, 6, 5 };
int d8 [] = { 5, 6, 7, 8, 9, 10, 11 };
int d9 [] = { 5, 6, 7, 8, 9, 10 };
int dd [] = { 4 };

void display_digit(int arr[], int size)
{
  for (int i = 0; i < size; i++)
    digitalWrite(arr[i], HIGH);
}

void display(int n)
{

  switch (n)
  {
  case 0:
    display_digit(d0, sizeof(d0) / sizeof(*d0));
    break;
  case 1:
    display_digit(d1, sizeof(d1) / sizeof(*d1));
    break;
  case 2:
    display_digit(d2, sizeof(d2) / sizeof(*d2));
    break;
  case 3:
    display_digit(d3, sizeof(d3) / sizeof(*d3));
    break;
  case 4:
    display_digit(d4, sizeof(d4) / sizeof(*d4));
    break;
  case 5:
    display_digit(d5, sizeof(d5) / sizeof(*d5));
    break;
  case 6:
    display_digit(d6, sizeof(d6) / sizeof(*d6));
    break;
  case 7:
    display_digit(d7, sizeof(d7) / sizeof(*d7));
    break;
  case 8:
    display_digit(d8, sizeof(d8) / sizeof(*d8));
    break;
  case 9:
    display_digit(d9, sizeof(d9) / sizeof(*d9));
    break;
  case -1:
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    break;
  }
}

void displayNumber(int number)
{
  
}

void setup()
{
  int i;
  for (i = 4; i <= 11; i++)
    pinMode(i, OUTPUT);
}

void loop()
{
  int n = 0;
  n = 0;
  while (true)
  {
    display(-1);
    display(n);
    delay(1000);
    n = (n + 1) % 10;
  }
}
