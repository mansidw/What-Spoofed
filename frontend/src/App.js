import { useRef } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const func = async () => {
    console.log(emailRef.current.value)
    console.log(passRef.current.value)
    const response = await axios.get(
      `/data?email=${emailRef.current.value}&password=${passRef.current.value}`,
    )
    console.log('', response.data)
  }
  const emailRef = useRef(null)
  const passRef = useRef(null)
  return (
    <div className="App">
      <div id="container">
        <div id="spooky">
          <div id="body">
            <div id="eyes"></div>
            <div id="mouth"></div>
            <div id="feet">
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        </div>
        <div id="shadow"></div>
        <div id="spooky">
          <form>
            <div class="group">
              <input type="text" ref={emailRef} required />
              <span class="highlight"></span>
              <span class="bar"></span>
              <label>Email</label>
            </div>

            <div class="group">
              <input type="text" ref={passRef} required />
              <span class="highlight"></span>
              <span class="bar"></span>
              <label>Password</label>
            </div>
          </form>
          <a class="Button White" onClick={func}>
            Check!
          </a>
        </div>
        {/* <div id="text">Happy Halloween!</div> */}
      </div>
    </div>
  )
}

export default App
