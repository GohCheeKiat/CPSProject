import React, {useState, useEffect} from "react";
// import Card from "@leafygreen-ui/card";
// import { H2 } from "@leafygreen-ui/typography";
// import PostSummary from "../components/PostSummary";
import { baseUrl } from "../config";

export default function App() {
  let [posts, setPosts] = useState([]);

  useEffect(() => {
    const loadPosts = async () => {
      let results = await fetch(`${baseUrl}/posts/latest`).then(resp => resp.json());
      setPosts(results);
    }

    loadPosts();
  }, []);

  let calculateAnimationDuration = (medianTemperature, medianHumidity) => {


    let tempSegments = [20, 25, 30, 35, 40]; // Example temperature segments
    let humiditySegments = [30, 40, 50, 60, 70]; // Example humidity segments
    let durationSegments = [4, 2, 1, 0.5, 0.1]; // Corresponding duration segments in seconds

    let duration = 0;

    for (let i=tempSegments.length - 1; i>=0; i--) {
      if (medianTemperature >= tempSegments[i] || medianHumidity >= humiditySegments[i]) {
        duration = durationSegments[i]
        break;
      }
    }

    return duration;
  }

  let fanSpeed = (medianTemperature, medianHumidity) => {
    const duration = calculateAnimationDuration(medianTemperature, medianHumidity);
    // eslint-disable-next-line
    if (duration == 0) {
      return "is OFF";
    }
    else {
      let durationSegments = [4, 2, 1, 0.5, 0.1];
      return `speed is ${durationSegments.indexOf(duration) + 1}/5`;
    }
  }


  return (
    <React.Fragment>
      {/* <H2>Fan simulation</H2> */}
      <div>
        {posts.map(post => {


          return(
            <div>
              <div className="fan fan-1">
                <div className="core-part" style={{ animationDuration: `${calculateAnimationDuration(post.medianTemperature, post.medianHumidity)}s` }}>
                  <div className="wing wing-1"></div>
                  <div className="wing wing-2"></div>
                  <div className="wing wing-3"></div>
                  <div className="wing wing-4"></div>
                  <div className="wing wing-5"></div>
                  <div className="wing wing-6"></div>
                </div>
            </div>
            <div className="fan fan-2"></div>
            <div className="fan fan-3"></div>

            <button className="display-button" style={{marginBottom: "7px"}}>Temperature is - {post.medianTemperature} &nbsp; &nbsp;  Humidity is - {post.medianHumidity}</button>
            <button className="display-button">Fan {fanSpeed(post.medianTemperature, post.medianHumidity)}</button>

          </div>
            
          )
        })}
      </div>
    </React.Fragment>
  )
}
