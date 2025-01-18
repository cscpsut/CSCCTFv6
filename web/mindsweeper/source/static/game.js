document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('game-grid');
    let gameBoard = [];
    let revealedCells = [];
    let size = 10;

    function createMessageOverlay(message, isWin = false) {
        const overlay = document.createElement('div');
        overlay.className = `game-message-overlay ${isWin ? 'win' : 'lose'}`;
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = message;
        
        const newGameBtn = document.createElement('button');
        newGameBtn.className = 'retro-button';
        newGameBtn.textContent = 'Okay';
        newGameBtn.onclick = () => {
            overlay.remove();
            // initializeGame();
        };
        
        content.appendChild(messageText);
        content.appendChild(newGameBtn);
        overlay.appendChild(content);
        
        return overlay;
    }
    
    // Initialize game state
    function initializeGame() {
        grid.innerHTML = '';
        revealedCells = Array(size).fill().map(() => Array(size).fill(false));
        fetch('/start-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            gameBoard = data;
            createGrid();
        })
        .catch(error => console.error('Error:', error));
    }

    // Create the visual grid
    function createGrid() {
        grid.style.gridTemplateColumns = `repeat(${size}, 30px)`;
        
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                // Right click event for flagging
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    toggleFlag(cell);
                });
                
                // Left click event for revealing
                cell.addEventListener('click', () => {
                    if (!cell.classList.contains('flagged')) {
                        revealCell(i, j);
                    }
                });
                
                grid.appendChild(cell);
            }
        }
    }

    // Toggle flag on right click
    function toggleFlag(cell) {
        if (!cell.classList.contains('revealed')) {
            cell.classList.toggle('flagged');
        }
    }

    // Get adjacent mine count
    function getAdjacentMines(row, col) {
        let count = 0;
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                const newRow = row + i;
                const newCol = col + j;
                if (newRow >= 0 && newRow < size && newCol >= 0 && newCol < size) {
                    if (gameBoard[newRow][newCol] === -1) {
                        count++;
                    }
                }
            }
        }
        return count;
    }

    // Flood fill algorithm for revealing empty cells
    function floodFill(row, col) {
        if (row < 0 || row >= size || col < 0 || col >= size || revealedCells[row][col]) {
            return;
        }

        const cell = grid.children[row * size + col];
        if (cell.classList.contains('flagged')) {
            return;
        }

        revealedCells[row][col] = true;
        cell.classList.add('revealed');

        const adjacentMines = getAdjacentMines(row, col);
        if (adjacentMines > 0) {
            cell.textContent = adjacentMines;
            cell.classList.add(`mines-${adjacentMines}`);
            return;
        }

        // If no adjacent mines, recursively reveal neighbors
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                floodFill(row + i, col + j);
            }
        }
    }

    // Reveal cell logic
    function revealCell(row, col) {
        if (revealedCells[row][col]) {
            return;
        }
    
        const cell = grid.children[row * size + col];
        
        if (gameBoard[row][col] === -1) {
            // Game Over - Hit a mine
            revealAllMines();
            cell.classList.add('mine', 'exploded');
            const overlay = createMessageOverlay('Game Over! You hit a mine!');
            grid.parentElement.appendChild(overlay);
            return;
        }
    
        floodFill(row, col);
        checkWin();
    }

    // Reveal all mines when game is over
    function revealAllMines() {
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (gameBoard[i][j] === -1) {
                    const cell = grid.children[i * size + j];
                    cell.classList.add('revealed', 'mine');
                }
            }
        }
    }

    // Check if player has won
    function checkWin() {
        let unrevealedSafeCells = false;
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (gameBoard[i][j] !== -1 && !revealedCells[i][j]) {
                    unrevealedSafeCells = true;
                    break;
                }
            }
        }
        
        if (!unrevealedSafeCells) {
            updateLeaderboard();
            const overlay = createMessageOverlay('Congratulations! You won!', true);
            grid.parentElement.appendChild(overlay);
        }
    }

    function updateLeaderboard() {
        fetch('/update-score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Leaderboard updated successfully');
            }
        })
        .catch(error => console.error('Error updating leaderboard:', error));
    }



    // Start new game button
    document.getElementById('start-game').addEventListener('click', initializeGame);

    // Initialize first game
    initializeGame();
});