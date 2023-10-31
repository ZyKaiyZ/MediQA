<script setup>
import axios from 'axios';

</script>
<template>
    <div class="main-body">
        <div class="question">
            Question : 
        </div>
        <div class="answer">
            Answer : 
        </div>
        <div class="prompt-area">
            <input type="text" name="input" class="input-prompt">
            <font-awesome-icon icon="fa-solid fa-paper-plane" class="send-btn"/>
        </div>
    </div>
</template>
<style scoped>
    .main-body {
        display: inherit;
        margin: auto;
        padding: 10px;
        color: white;
        border-radius: 0px 0px 15px 15px;
        width: 70%;
        background-color: #343541;
        height: 83vh;
    }

    .question{
        margin: auto;
        text-align: left;
        font-size: 30px;
        width: 95%;
        height: 20vh;
    }

    .answer{
        margin: auto;
        text-align: left;
        font-size: 30px;
        width: 95%;
        height: 20vh;
    }

    .prompt-area{
        display: flex;
        justify-content: center;
        margin-top: 35vh;
        text-align: center;
        width: 100%;
        font-size: 25px;
    }

    .input-prompt{
        background-color: rgba(125, 125, 138, 0.8);
        border-radius: 5px 0px 0px 5px;
        border: none;
        caret-color: white;
        color: white;
        outline: none;
        padding: 5px 10px 5px 10px;
        width: 70%;
    }

    .send-btn{
        background-color: rgba(125, 125, 138, 0.8);
        border-radius: 0px 5px 5px 0px;
        padding: 5px 10px 5px 7px;
        outline: none;
    }

    .send-btn:hover{
        cursor: pointer;
        background-color: #7db926;
    }

    .send-btn:active{
        transform: translateX(0.5px);
    }
</style>

<div class="inputWithin">
    <input type="text" class=" inputPaddingRight" placeholder="right button">
    <button class="btn">button</button>
  </div>