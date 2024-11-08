// Add Question Button Event
document.getElementById('addQuestionButton').addEventListener('click', function() {
    const questionsContainer = document.getElementById('questionsContainer');

    // Create the question block
    const questionBlock = document.createElement('div');
    questionBlock.className = 'question-block';

    // Question label and input
    const questionLabel = document.createElement('label');
    questionLabel.textContent = 'Question Text:';
    
    const questionInput = document.createElement('input');
    questionInput.type = 'text';
    questionInput.name = 'questionText';
    questionInput.className = 'form-control';
    questionInput.required = true;

    // Question type label and select
    const questionTypeLabel = document.createElement('label');
    questionTypeLabel.textContent = 'Question Type:';
    
    const questionTypeSelect = document.createElement('select');
    questionTypeSelect.name = 'questionType';
    questionTypeSelect.className = 'form-control';
    questionTypeSelect.required = true;

    const options = [
        { value: '', text: 'Select' },
        { value: 'text', text: 'Text' },
        { value: 'singleChoice', text: 'Multiple Choice (Single Answer)' },
        { value: 'multipleChoice', text: 'Multiple Choice (Multiple Answers)' }
    ];
    
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.text;
        questionTypeSelect.appendChild(option);
    });

    // Remove Question Button
    const removeQuestionButton = document.createElement('button');
    removeQuestionButton.type = 'button';
    removeQuestionButton.textContent = '×';
    removeQuestionButton.className = 'remove-question-btn';
    removeQuestionButton.addEventListener('click', function() {
        questionBlock.remove();
    });

    // Append elements to the question block
    questionBlock.appendChild(questionLabel);
    questionBlock.appendChild(questionInput);
    questionBlock.appendChild(questionTypeLabel);
    questionBlock.appendChild(questionTypeSelect);
    questionBlock.appendChild(removeQuestionButton);

    questionsContainer.appendChild(questionBlock);

    // Handle question type selection
    questionTypeSelect.addEventListener('change', function() {
        const existingOptionsContainer = questionBlock.querySelector('.optionsContainer');
        if (existingOptionsContainer) existingOptionsContainer.remove();

        if (this.value === 'text') {
            const textArea = document.createElement('textarea');
            textArea.className = 'form-control';
            textArea.placeholder = 'User will enter their response here...';
            textArea.rows = 3;
            textArea.disabled = true;
            questionBlock.appendChild(textArea);
        } else if (this.value === 'singleChoice' || this.value === 'multipleChoice') {
            const optionContainer = document.createElement('div');
            optionContainer.className = 'optionsContainer';
            questionBlock.appendChild(optionContainer);

            const addOptionButton = document.createElement('button');
            addOptionButton.type = 'button';
            addOptionButton.textContent = 'Add Option';
            addOptionButton.className = 'btn btn-info';
            optionContainer.appendChild(addOptionButton);

            addOptionButton.addEventListener('click', function() {
                const optionWrapper = document.createElement('div');
                optionWrapper.className = 'option-wrapper';

                const optionInput = document.createElement('input');
                optionInput.type = 'text';
                optionInput.name = 'optionText';
                optionInput.placeholder = 'Option text';
                optionInput.className = 'form-control';
                optionInput.required = true;

                const removeOptionButton = document.createElement('button');
                removeOptionButton.type = 'button';
                removeOptionButton.textContent = '×';
                removeOptionButton.className = 'remove-option-btn';
                removeOptionButton.addEventListener('click', function() {
                    optionWrapper.remove();
                });

                optionWrapper.appendChild(optionInput);
                optionWrapper.appendChild(removeOptionButton);
                optionContainer.appendChild(optionWrapper);
            });
        }
    });
});

// Form Submission Event
document.getElementById('surveyForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Collect survey data
    const surveyTitle = document.getElementById('surveyTitle').value;
    const surveyDescription = document.getElementById('surveyDescription').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    const questions = [];
    document.querySelectorAll('.question-block').forEach((questionBlock) => {
        const questionText = questionBlock.querySelector('input[name="questionText"]').value;
        const questionType = questionBlock.querySelector('select[name="questionType"]').value;
        let options = [];

        if (questionType === 'singleChoice' || questionType === 'multipleChoice') {
            questionBlock.querySelectorAll('.option-wrapper input[name="optionText"]').forEach(optionInput => {
                options.push(optionInput.value);
            });
        }

        questions.push({
            text: questionText,
            type: questionType,
            options: options
        });
    });

    const surveyData = {
        title: surveyTitle,
        description: surveyDescription,
        start_date: startDate,
        end_date: endDate,
        questions: questions
    };

    // Send data to the server
    fetch('/create-survey', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(surveyData)
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `/view-survey/${data.survey_id}`;
    })
    .catch(error => console.error('Error:', error));
});
