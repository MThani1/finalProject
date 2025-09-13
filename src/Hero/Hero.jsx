import React from 'react'
import './Hero.css'
import Car from '../car/Car'
const Hero = () => {
  return (
    <section className="wrapper">
    <div className="flexCenter paddings innerWidth">
      <h1 className=" yap flexCenter">
        NUMBER OF AVAILABLE SPACES 
      </h1>

    </div>
    <div className="cycle paddings flexColCenter">
      <h2 className="spaces"><Car /></h2>
    </div>

  </section>
  )
}

export default Hero