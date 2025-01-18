const BLANK_CELL_NUM = 8;

function getRandomWord(){
    let arr = ['csc', 'ctf', 'APT'];
    
    return arr[Math.floor(Math.random()*(arr.length+1))];
}

function getShuffledPuzzle() {
    const values = [0, 1, 2, 3, 4, 5, 6, 7, 8];
  
    const rowOne = [],
        rowTwo = [],
        rowThree = [];
  
    while (values.length) {
        const random = Math.floor(Math.random() * values.length);
    
        if (rowOne.length < 3) {
            rowOne.push(values.splice(random, 1)[0]);
        } else if (rowTwo.length < 3) {
            rowTwo.push(values.splice(random, 1)[0]);
        } else {
            rowThree.push(values.splice(random, 1)[0]);
        }
    }
  
    return [rowOne, rowTwo, rowThree];
};

function flattenArray(arr){
    return arr.reduce((flatArr, subArr) => flatArr.concat(subArr), []);
};
  
function getInversionsCount(arr){
    arr = flattenArray(arr).filter(n => n !== BLANK_CELL_NUM);
  
    const inversions = [];
  
    for (let i = 0; i < arr.length - 1; i++) {
        const currentValue = arr[i];
        const currentInversions = arr.filter(
            (val, j) => i < j && val < currentValue
        );
        inversions.push(currentInversions.length);
    }
  
    const inversionsCount = inversions.reduce((total, val) => total + val, 0);
  
    return inversionsCount;
};
  
function isSolvable(puzzle){
    return getInversionsCount(puzzle) % 2 === 0;
};
  
function getPuzzle(){
    let puzzle = getShuffledPuzzle();
  
    while (!isSolvable(puzzle)) {
        puzzle = getShuffledPuzzle();
    }
  
    return puzzle;
};


export {getRandomWord, getPuzzle, BLANK_CELL_NUM}