<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { baseUrl } from '../main';

let question = ref('');
let answer = ref('');
let inputQuestion = ref('');

const UpdateQuestionAndAnswer = () => {
    question.value = inputQuestion.value;
    getAnswer();
    inputQuestion.value = "";
}

const getAnswer = async () => {
    try {
        const response = await axios.post(`${ baseUrl }/ask`, {
            "question": question.value
        });
        answer.value = response.data.result;
    } catch (error) {
        console.error('Error fetching answer:', error);
    }
}
</script>
<template>
    <div class="main-body">
        <div class="question">
            <p class="title">Question</p>
            <p class="text">{{ question }}</p>
        </div>
        <div class="answer">
            <p class="title">Answer</p>
            <p class="text">{{ answer }}</p>
        </div>
        <div class="prompt-area">
            <input v-model="inputQuestion" type="text" name="input" class="input-prompt" placeholder="Input your question">
            <font-awesome-icon icon="fa-solid fa-paper-plane" class="send-btn" @click="UpdateQuestionAndAnswer"/>
        </div>
    </div>
</template>
<style scoped>
    .main-body {
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
    .title{
        color: #7db926;
        font-weight: bold;
        font-size: 30px;
        margin-top: 3px;
        margin-bottom: 7px;
    }
    .text{
        font-size: 20px;
        margin-top: 3px;
        margin-bottom: 3px;
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

    .input-prompt::placeholder{
        color: rgba(255, 255, 255, 0.534);
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