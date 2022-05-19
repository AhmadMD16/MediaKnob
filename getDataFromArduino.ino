// Setting input pins for the rotary encoder
#define inputCLK 4
#define inputDT 3
#define inputSW 5

// Button timing variables
#define debounce 20
#define double_click_gap 250
#define holdTime 1000

// Media and volume variables
int volume = 20;
int next = 0;
int prev = 0;
int pause = 0;
int play = 0;
int previousStateCLK;
int currentStateCLK;
int mode = 1;
int max_modes = 3;

// Other button variables
boolean buttonVal = HIGH; // reads value from button
boolean buttonLast = HIGH; // buffered value of the button's previous state
boolean DCwaiting = false; // whether we're waiting for a double click (down)
boolean DConUp = false; // whether to register a double click on next release, or whether to wait and click
boolean singleOK = true; // whether it's OK to do a single click
long downTime = -1; // time the button was pressed down
long upTime = -1; // time the button was released
boolean ignoreUp = false; // whether to ignore the button release because the click+hold was triggered
boolean waitForUp = false; // when held, whether to wait for the up event
boolean holdEventPast = false; // whether or not the hold event happened already
boolean longHoldEventPast = false;// whether or not the long hold event happened already

//-----------------------------------------

void setup()
{
  pinMode(inputCLK, INPUT);
  pinMode(inputDT, INPUT);
  pinMode(inputSW, INPUT_PULLUP);
  digitalWrite(inputSW, HIGH );
  previousStateCLK = digitalRead(inputCLK);
  Serial.begin(9600);
}

void loop()
{
  // Read the current state of inputCLK
  currentStateCLK = digitalRead(inputCLK);
  // If the previous and the current state of the inputCLK are different then a pulse has occured
  if (currentStateCLK != previousStateCLK)
  {
    // If the inputDT state is different than the inputCLK state then
    // the encoder is rotating counterclockwise
    if (digitalRead(inputDT) != currentStateCLK)
    {
      rotateRight();
    }
    else
    {
      rotateLeft();
    }
    // Update previousStateCLK with the current state
    previousStateCLK = currentStateCLK;
    // Sends desired volume to serial monitor
    Serial.println(volume);
  }
  // Checks what actions are performed
  int b = checkButton();
  if (b == 1) singleClick();
  if (b == 2) doubleClick();
  if (b == 3) buttonHold();
}

// Single click will pause and play media
void singleClick()
{
  pause++;
  if (pause >= 2)
  {
    pause = 0;
    Serial.println("play");
  }
  else
    Serial.println("pause");
}

// Mutes the audio
void doubleClick()
{
  Serial.println("mute");
}

// When you hold the button, the program will switch to what I call "Shuffle mode" (mode 2)
void buttonHold()
{
  mode++;
  if (mode >= max_modes)
  {
    mode = 1;
    Serial.println("mode1");
  }
  else
    Serial.println("mode2");
}

// This function detects if the button is pressed once, twice or if you're holding it
int checkButton()
{
  int event = 0;
  buttonVal = digitalRead(inputSW);
  if (buttonVal == LOW && buttonLast == HIGH && (millis() - upTime) > debounce)
  {
    downTime = millis();
    ignoreUp = false;
    waitForUp = false;
    singleOK = true;
    holdEventPast = false;
    longHoldEventPast = false;
    if ((millis() - upTime) < double_click_gap && DConUp == false && DCwaiting == true) DConUp = true;
    else DConUp = false;
    DCwaiting = false;
  }
  else if (buttonVal == HIGH && buttonLast == LOW && (millis() - downTime) > debounce)
  {
    if (not ignoreUp)
    {
      upTime = millis();
      if (DConUp == false) DCwaiting = true;
      else
      {
        event = 2;
        DConUp = false;
        DCwaiting = false;
        singleOK = false;
      }
    }
  }
  if ( buttonVal == HIGH && (millis() - upTime) >= double_click_gap && DCwaiting == true && DConUp == false && singleOK == true)
  {
    event = 1;
    DCwaiting = false;
  }
  if (buttonVal == LOW && (millis() - downTime) >= 1000)
  {
    if ((millis() - downTime) >= holdTime)
    {
      if (not longHoldEventPast)
      {
        waitForUp = true;
        ignoreUp = true;
        DConUp = false;
        DCwaiting = false;
        event = 3;
        longHoldEventPast = true;
      }
    }
  }
  buttonLast = buttonVal;
  return event;
}

// If rotated CCW it will decrease the volume(mode 1) or play previous song(mode 2)
void rotateLeft()
{
  switch (mode)
  {
    // Decrease the volumeume.
    case 1:
      if (volume > 0)
      {
        volume = volume - 1;
      }
      break;

    // Previous song
    case 2:
      prev = prev - 1;
      if (prev <= -4)
      {
        Serial.println("prevtrack");
        prev = 0;
      }
      break;
  }
}

// If rotated CW it will increase the volume(mode 1) or play next song(mode 2)
void rotateRight()
{
  switch (mode)
  {
    // Increase the volumeume.
    case 1:
      if (volume < 100)
      {
        volume = volume + 1;
      }
      break;
    // Next song
    case 2:
      next = next + 1;
      if (next >= 4)
      {
        Serial.println("nexttrack");
        next = 0;
      }
      break;
  }
}
