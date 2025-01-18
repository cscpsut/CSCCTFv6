const words = [
    'H04X', 'habema', 'AvA_l4nch', 'Loki', 'Yazam', 'Be5a', 'Jana', 'KAIOKEN',
    'l0mb4rd', 'lana', 'Reddington', 'safareto', 'Salim_Shady', 'hamoor', 'niddehalas']

export default function getRandomWord(){
    return words[Math.floor(Math.random()*(words.length+1))];
}