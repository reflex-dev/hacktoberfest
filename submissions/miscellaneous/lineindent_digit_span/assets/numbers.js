// JavaScript source code for Digit Span Game.
// To be used in combination with Reflex front end. 

let currentLevel = 2;
let inputLength = 2;
let sequence = [];
let numberArray = [];
let numLives = 3;

const digit = document.getElementById("digit");
const startButton = document.getElementById("start");
const checkButton = document.getElementById("check");
checkButton.disabled = true;
const userSequence = document.getElementById("userSequence");


const lives = document.getElementById("lives")
const level = document.getElementById("level")

const result = document.getElementById("result")

userSequence.addEventListener("input", function() {
    var inputValue = userSequence.value;
    this.value = this.value.replace(/\D/g, "");
    if (inputValue.length > inputLength) {
        userSequence.value = inputValue.slice(0, inputLength);
        }
    
    if (inputValue.length === inputLength) {
        checkButton.disabled = false;
    }
});


async function generateRandomSequence(length) {
  startButton.disabled = true;
  userSequence.disabled = true;
  checkButton.disabled = true;
  for (let i = 0; i < length; i++) {
      rando = Math.floor(Math.random() * 10);
      sequence.push(rando);
      digit.textContent = rando;
      await new Promise(resolve => setTimeout(resolve, 500));
      digit.textContent = '';
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    digit.textContent = ''
    userSequence.disabled = false;
    checkButton.disabled = false;
    
}

function startNewLevel() {
   digit.style.color = ""
   result.textContent = ""
   generateRandomSequence(currentLevel);
}


function checkIfMatch() {
    if (sequence.length != numberArray.length) {
        return false;
    }

    for (let i = 0; i < sequence.length; i++) {
        if (sequence[i] !== numberArray[i]) {
            return false;
        } 
    }

    return true;
}

async function checkUserSequence() {
    checkButton.disabled = true;
    for (let i = 0; i < userSequence.value.length; i++) {
        const character = userSequence.value.charAt(i);
        const digit = parseInt(character, 10);
        if (!isNaN(digit)) {
            numberArray.push(digit); 
          }
    }
    userSequence.value = ''

    const isMatch = checkIfMatch()

    if (isMatch) {
        digit.textContent = `✓`;
        digit.style.color = "green"
        await new Promise(resolve => setTimeout(resolve, 1000));
        goToNextLevelSettings()
        
        
    } else {
        if (numLives === 1) {
            digit.textContent = `X`;
            digit.style.color = "red"
            result.textContent = `You completed round ${currentLevel - 2} and a digit span of ${currentLevel - 1}. To start over, press play.`
            restGameSettings();
        } else {
            numberArray.length = 0;
            numLives -= 1
            lives.textContent = numLives.toString()
            result.textContent = 'Incorrect digit sequence. Try again!'
            await new Promise(resolve => setTimeout(resolve, 2000));
            result.textContent = ''
            
        }

    }

}


function goToNextLevelSettings() {
    if (currentLevel === 10) {
        level.textContent = 10
        result.textContent = `Congrats! You reached the maximium span of 10 digits!!`
    } else {
        sequence.length = 0;
        numberArray.length = 0;
        startButton.disabled = false;
        currentLevel += 1
        inputLength += 1    
        level.textContent = currentLevel - 1

    }
}

function restGameSettings() {
    currentLevel = 2;
    inputLength = 2;
    sequence = [];
    numberArray = [];
    numLives = 3;

    lives.textContent = numLives.toString()
    level.textContent = '1'
    startButton.disabled = false

}


