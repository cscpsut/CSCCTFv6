import { useRef } from 'react';
import styles from "./RuleLocation.module.css";
import Rule from "../Rule";
import ReloadButton from '../../components/ReloadButton';


const locations = {
    'Palestine': [31.5082, 34.4654],
}

export default class RuleLocation extends Rule{
    constructor(){
        super("Your password must contain the name of the country at this latitude and longitude.");
        this.keys = Object.keys(locations);
        this.locationName = this.keys[Math.floor(Math.random()*this.keys.length)];
        console.log("Country:", this.locationName);

        this.renderItem = ({regenerateRule, correct}) => <Location locationName={this.locationName} regenerate={()=>regenerateRule(this.num)} correct={correct}/>
        // this.num is the rule number that is dynamically set later
    }

    regenerate(){
        this.locationName = this.keys[Math.floor(Math.random()*this.keys.length)];
        console.log("Country:", this.locationName);
    }

    check = (txt) => {
        let r = RegExp(`(?:${this.locationName})`, "i");
        return r.test(txt);
    }
}


function Location({locationName, regenerate, correct}){
    const latitude = locations[locationName][0];
    const longitude = locations[locationName][1];
    const reloadsLeft = useRef(3);    

    return (
        <div className={styles.location_wrapper}>
            <div className={styles.location}>
                {latitude}, {longitude}
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