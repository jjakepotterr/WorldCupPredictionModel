// The dining room (handles our presentation)

import { useState } from 'react'
import axios from 'axios'  // important library in this case as it uses HTTP requests (GET,POST,PUT,DELETE) from the react app to a server
import './App.css'

function App() {  // how app will function
  const [input, setInput] = useState('')          // Logic and variables go here above return 

  const [messages, setMessages] = useState([])

  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {               // Async acts as a buffer, When you call onto Flask to do its job async allows frontend to wait on backend till completion is reached
    if (input === "") {                           // always '===' instead of '==' in JS because it can cause weird bugs, '===' is strict and checks both value and type
      return                          // if input is empty nothing happens
    }
    setMessages(prev => [...prev, { "role": "user", "text": input }])         //the user's message is added to messages state

    setLoading(true)             // loading process begins

    setInput('')                 // after input is cleared again, but since state updates asynchronusly it is scheduled to clear after the next render.
    // so input still holds the original typed value like "Brazil" for example 

    try {                          // trial and error system/contact with backend
      const response = await axios.post('http://localhost:5001/predict', {      // communicates to backend. Tells Flask to do its thing and figure out the logic before returning info to frontend
        team: input         // sends specifically what user typed as team
      })

      const data = response.data      // shows the Flask data returned
      setMessages(prev => [...prev, { role: 'bot', text: data }])  // store the data as the robotic flask response (not human language yet) in our messages array
    } catch (error) {                                            // in the case something goes wrong on the backend
      setMessages(prev => [...prev, { role: 'bot', text: { error: error.message + ' | ' + (error.response?.data?.error || 'no response') } }]) //this message is sent
    } finally {
      setLoading(false)        // loading phase ends when everything falls through our trial and error system
    }
  }

  //TEAM COLORS
  const teamColor = (team) => {
    const colors = {
      // Group favorites & big nations
      'Brazil': '#f3ff13',        // iconic yellow
      'France': '#002395',        // deep blue (Les Bleus)
      'Argentina': '#74ACDF',     // sky blue albiceleste
      'Germany': '#000000',       // classic black
      'Spain': '#AA151B',         // red of the flag
      'England': '#CF081F',       // St George red
      'Portugal': '#006600',      // dark green
      'Netherlands': '#FF6600',   // oranje
      'Belgium': '#000000',       // black of the flag
      'Italy': '#003399',         // azzurri blue

      // Americas
      'USA': '#B22234',           // stars & stripes red
      'Mexico': '#006847',        // deep green
      'Canada': '#FF0000',        // maple leaf red
      'Argentina': '#74ACDF',     // sky blue
      'Colombia': '#FCD116',      // yellow
      'Ecuador': '#FFD100',       // yellow
      'Uruguay': '#5EB6E4',       // light blue
      'Paraguay': '#D52B1E',      // red
      'Bolivia': '#D52B1E',       // red
      'Panama': '#DA121A',        // red

      // Africa
      'Morocco': '#006233',       // green
      'Senegal': '#00853F',       // green
      'Ghana': '#006B3F',         // green (flag)
      'Ivory Coast': '#F77F00',   // orange
      'South Africa': '#007A4D',  // green
      'Egypt': '#CE1126',         // red
      'Tunisia': '#E70013',       // red
      'Algeria': '#006233',       // green
      'DR Congo': '#007FFF',      // blue
      'Cameroon': '#007A5E',      // green

      // Asia
      'Japan': '#BC002D',         // red (rising sun)
      'South Korea': '#003478',   // blue
      'Saudi Arabia': '#006C35',  // green
      'Iran': '#239F40',          // green
      'Australia': '#FFD700',     // gold
      'Qatar': '#8D1B3D',         // maroon
      'Iraq': '#CE1126',          // red
      'Uzbekistan': '#1EB53A',    // green

      // Europe (rest)
      'Croatia': '#FF0000',       // red checkers
      'Switzerland': '#FF0000',   // red cross
      'Sweden': '#006AA7',        // blue
      'Norway': '#EF2B2D',        // red
      'Turkey': '#E30A17',        // red crescent
      'Austria': '#ED2939',       // red
      'Scotland': '#003399',      // blue
      'Bosnia and Herzegovina': '#002395', // blue
      'Czech Republic': '#D7141A', // red
      'Slovakia': '#0B4EA2',      // blue

      // Others
      'Jordan': '#007A3D',        // green
      'Cape Verde': '#003893',    // blue
      'Haiti': '#00209F',         // blue
      'Curacao': '#002B7F',       // blue
      'New Zealand': '#00247D',   // blue
      'Congo DR': '#007FFF',      // blue
    }
    return colors[team] || '#888888'
  }

  return (
    <div className="container">
      <h1>⚽ 2026 World Cup Predictor</h1>
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index}>
            {msg.role === 'user' && (
              <div className="user-msg">
                <div className="user-bubble">{msg.text}</div>
              </div>
            )}
            {msg.role === 'bot' && (
              <div className="bot-msg">
                <div className="bot-bubble">
                  {msg.text.error && <p className="error">{msg.text.error}</p>}
                  {msg.text.win_probability && (
                    <>
                      <p className="probability">{msg.text.team}: {msg.text.win_probability}%</p>
                      <p className="explanation">{msg.text.explanation}</p>
                      <p className="comparison">Closest comparison: {msg.text.closest_team} at {msg.text.closest_prob}%</p>
                      <p className="bar-label">🟡 {msg.text.team}</p>
                      <div className="bar-container">
                        <div style={{ width: `${msg.text.win_probability}%`, background: teamColor(msg.text.team), height: '14px', borderRadius: '8px' }} />
                      </div>
                      <p className="bar-label" style={{ marginTop: '6px' }}>🔵 {msg.text.closest_team}</p>
                      <div className="bar-container">
                        <div style={{ width: `${msg.text.closest_prob}%`, background: teamColor(msg.text.closest_team), height: '14px', borderRadius: '8px' }} />
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && <p className="analyzing">⚽ Analyzing...</p>}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask about any team... e.g. What are Brazil's chances?"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}

export default App // other files that import from this will receive these important app functionalities