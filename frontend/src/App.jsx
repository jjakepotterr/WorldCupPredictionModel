// The dining room (handles our presentation)

import { useState } from 'react' 

function App() {  // how app will function
  const [input, setInput] = useState('')          // Logic and variables go here above return 

  const [messages, setMessages] = useState([])

  const [loading, setLoading] = useState(false)
  return (                                         // only used for HTML style/JSX (what user sees)

  )
}

export default App // other files that import from this will receive these important app functionalities