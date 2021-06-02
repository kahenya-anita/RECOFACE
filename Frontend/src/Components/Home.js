import React, {useState} from 'react';
import {FaCameraRetro} from 'react-icons/fa';
import Video from '../videos/video.mp4';
import {HeroContainer,HeroBg, VideoBg,HeroContent, HeroH1,HeroH2,HeroP,HeroBtnWrapper} from './HomeElements';


function Home() {
    const [hover, setHover] = useState(false)

    const onHover = () => {
        setHover(!hover)
    }
    return (
        <HeroContainer>
            <HeroBg>
                <VideoBg autoplay loopd muted src={Video} type="video/mp4"/>
            </HeroBg>
            <HeroContent>
                <HeroH1>Pick a photo</HeroH1>
                <HeroH2>Or take a selfie</HeroH2>
                <HeroP>And let us a find a match online.</HeroP>
                <HeroBtnWrapper>Take a selfie <FaCameraRetro/>?</HeroBtnWrapper>
            </HeroContent>
            
        </HeroContainer>
    )
}

export default Home;
