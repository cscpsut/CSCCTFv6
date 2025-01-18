import { useRef } from 'react';
import Rule from "../Rule";
import styles from "./RuleRiddle.module.css";
import ReloadButton from '../../components/ReloadButton';


const riddles = [
    ["What CTF is the greatest CTF ever?", "CSCCTF"],
    ["Who has the best crocs at CSCCTF", "Saadi"],
    ["What is the best TV series? psst.. it's arcane", "arcane"],
    ["Which category should you solve first?", "misc"],
    ["Which category should leave to the end?", "crypto"],
    ["What is the flag format?", "CSCCTF"],
    ["Write \"I love CSCCTF\"", "I love CSCCTF"],
    ["Write \"I love habema\"", "I love habema"],
    ["Write \"I love AvA_l4nch\"", "I love AvA_l4nch"],
    ["Write \"I love Saadi\"", "I love Saadi"],
]


export default class RuleRiddle extends Rule{
    constructor(){
        super("Your password must contain the solution to the following question:");

        this.riddleNum = Math.floor(Math.random()*riddles.length);
        console.log("Riddle:", riddles[this.riddleNum][1]);
        this.renderItem = ({regenerateRule, correct}) => <Riddle riddleNum={this.riddleNum} regenerate={()=>regenerateRule(this.num)} correct={correct}/>
        // this.num is the rule number that is dynamically set later
        
    }

    regenerate(){
        this.riddleNum = Math.floor(Math.random()*riddles.length);
        console.log("Riddle:", riddles[this.riddleNum][1]);
    }

    check = (txt) => {
        let ans = riddles[this.riddleNum][1];
        let r = RegExp(`(?:${ans})`, "i");
        return r.test(txt);
    }
}

function Riddle({riddleNum, regenerate, correct}){
    const riddle = riddles[riddleNum][0];
    const reloadsLeft = useRef(3);

    return (
        <div className={styles.riddle_wrapper}>
            <div className={styles.riddle}>
                {riddle}
            </div>
            <ReloadButton 
                onClick={()=>{
                    if(reloadsLeft.current>0){
                        regenerate()
                        reloadsLeft.current--; 
                    }
                }} 
                hidden={correct} 
                reloadsLeft={reloadsLeft.current}
            />
        </div>
    )
}