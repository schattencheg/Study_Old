
int a = 7;
int b = 6;
int c = 5;
int d = 11;
int e = 10;
int f = 8;
int g = 9;
int dp = 4;

void display(int n)
{
    switch (n)
    {
    case 0:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        digitalWrite(e, HIGH);
        digitalWrite(f, HIGH);
        break;
    case 1:
        digitalWrite(b, HIGH);
        digitalWrite(c, HIGH);
        break;
    case 2:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(e, HIGH);
        digitalWrite(d, HIGH);
        break;
    case 3:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        digitalWrite(g, HIGH);
        break;
    case 4:
        digitalWrite(f, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(c, HIGH);
        break;
    case 5:
        digitalWrite(a, HIGH);
        digitalWrite(f, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        break;
    case 6:
        digitalWrite(a, HIGH);
        digitalWrite(f, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        digitalWrite(e, HIGH);
        break;
    case 7:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(c, HIGH);
        break;
    case 8:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        digitalWrite(e, HIGH);
        digitalWrite(f, HIGH);
        break;
    case 9:
        digitalWrite(a, HIGH);
        digitalWrite(b, HIGH);
        digitalWrite(g, HIGH);
        digitalWrite(c, HIGH);
        digitalWrite(d, HIGH);
        digitalWrite(f, HIGH);
        break;
    case -1:
        digitalWrite(a, LOW);
        digitalWrite(b, LOW);
        digitalWrite(g, LOW);
        digitalWrite(c, LOW);
        digitalWrite(d, LOW);
        digitalWrite(e, LOW);
        digitalWrite(f, LOW);
        break;
    }
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
    while (true)
    {
        display(-1);
        display(n);
        delay(2000);
        n = (n + 1) % 10;
    }
}
