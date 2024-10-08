document.getElementById('addQuestionButton').addEventListener('click', function() {
    const questionsContainer = document.getElementById('questionsContainer');

    // Create the question block
    const questionBlock = document.createElement('div');
    questionBlock.className = 'question-block';

    // Create the question label and input
    const questionLabel = document.createElement('label');
    questionLabel.textContent = 'Question Text:';
    
    const questionInput = document.createElement('input');
    questionInput.type = 'text';
    questionInput.name = 'questionText';
    questionInput.className = 'form-control';  // Bootstrap form control
    questionInput.required = true;

    // Create the question type label and select input
    const questionTypeLabel = document.createElement('label');
    questionTypeLabel.textContent = 'Question Type:';
    
    const questionTypeSelect = document.createElement('select');
    questionTypeSelect.name = 'questionType';
    questionTypeSelect.className = 'form-control';  // Bootstrap form control
    questionTypeSelect.required = true;

    const option0 = document.createElement('option');
    option0.textContent = 'Select';
    option0.value = '';
    option0.selected = true;

    const option1 = document.createElement('option');
    option1.value = 'text';
    option1.textContent = 'Text';
    

    const option2 = document.createElement('option');
    option2.value = 'singleChoice';
    option2.textContent = 'Multiple Choice (Single Answer)';

    const option3 = document.createElement('option');
    option3.value = 'multipleChoice';
    option3.textContent = 'Multiple Choice (Multiple Answers)';

    questionTypeSelect.appendChild(option0);
    questionTypeSelect.appendChild(option1);
    questionTypeSelect.appendChild(option2);
    questionTypeSelect.appendChild(option3);

    // Add the "Remove Question" button
    const removeQuestionButton = document.createElement('button');
    removeQuestionButton.type = 'button';
    removeQuestionButton.textContent = 'x';
    removeQuestionButton.className = 'remove-question-btn';  // Styled class
    removeQuestionButton.addEventListener('click', function() {
        questionBlock.remove(); // Remove the entire question block
    });

    

    // Append elements to the question block
    questionBlock.appendChild(questionLabel);
    questionBlock.appendChild(questionInput);
    questionBlock.appendChild(document.createElement('br'));
    questionBlock.appendChild(questionTypeLabel);
    questionBlock.appendChild(questionTypeSelect);
    questionBlock.appendChild(removeQuestionButton);

    questionsContainer.appendChild(questionBlock);

    // Add event listener to handle question type selection
    questionTypeSelect.addEventListener('change', function() {
        // Remove any existing input options when switching question types
        const existingOptionsContainer = questionBlock.querySelector('.optionsContainer');
        const existingTextAreaWrapper = questionBlock.querySelector('.textarea-wrapper');
        
        if (existingOptionsContainer) {
            existingOptionsContainer.remove();
        }
        if (existingTextAreaWrapper) {
            existingTextAreaWrapper.remove();
        }

        // If the question type is 'text', show a textarea
        if (this.value === 'text') {
            const textAreaWrapper = document.createElement('div');
            textAreaWrapper.className = 'textarea-wrapper'; // Wrapper for textarea and remove button

            const textArea = document.createElement('textarea');
            textArea.className = 'form-control'; // Bootstrap form control
            textArea.placeholder = 'User will enter their response here...';
            textArea.rows = 3;
            textArea.disabled = true; // Just for display, this would be enabled during the survey

            // Add a remove textarea button
            const removeTextAreaButton = document.createElement('button');
            removeTextAreaButton.type = 'button';
            removeTextAreaButton.textContent = '×'; // Cross symbol for removal
            removeTextAreaButton.className = 'remove-option-btn'; // Styled like remove option button
            removeTextAreaButton.addEventListener('click', function() {
                textAreaWrapper.remove(); // Remove the textarea
            });

            // Append textarea and remove button to wrapper
            textAreaWrapper.appendChild(textArea);
            textAreaWrapper.appendChild(removeTextAreaButton);
            questionBlock.appendChild(textAreaWrapper);
        }

        // If the question type is 'singleChoice' or 'multipleChoice', allow adding options
        if (this.value === 'singleChoice' || this.value === 'multipleChoice') {
            const optionContainer = document.createElement('div');
            optionContainer.className = 'optionsContainer';

            const addOptionButton = document.createElement('button');
            addOptionButton.type = 'button';
            addOptionButton.textContent = 'Add Option';
            addOptionButton.className = 'btn btn-info'; // Bootstrap button style
            optionContainer.appendChild(addOptionButton);

            questionBlock.appendChild(optionContainer);

            // Add event listener for adding options
            addOptionButton.addEventListener('click', function() {
                const optionWrapper = document.createElement('div');
                optionWrapper.className = 'option-wrapper'; // Styled for flex alignment

                const optionInput = document.createElement('input');
                optionInput.type = 'text';
                optionInput.name = 'optionText';
                optionInput.placeholder = 'Option text';
                optionInput.className = 'form-control'; // Bootstrap form control
                optionInput.required = true;

                const optionType = questionTypeSelect.value === 'singleChoice' ? 'radio' : 'checkbox';
                const optionElement = document.createElement('input');
                optionElement.type = optionType;
                optionElement.name = 'option';
                optionElement.disabled = true; // Just for display

                // Add a remove option button (styled as a cross)
                const removeOptionButton = document.createElement('button');
                removeOptionButton.type = 'button';
                removeOptionButton.textContent = '×'; // Cross symbol
                removeOptionButton.className = 'remove-option-btn'; // Styled class
                removeOptionButton.addEventListener('click', function() {
                    optionWrapper.remove(); // Remove the option
                });

                // Append option element and remove button to option wrapper
                optionWrapper.appendChild(optionElement);
                optionWrapper.appendChild(optionInput);
                optionWrapper.appendChild(removeOptionButton);
                optionContainer.insertBefore(optionWrapper, addOptionButton);
            });
        }
    });
});

// Handle form submission
/*document.getElementById('surveyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Survey Created Successfully!');
});*/


document.getElementById('surveyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    // Collect survey data
    const surveyTitle = document.getElementById('surveyTitle').value;
    const surveyDescription = document.getElementById('surveyDescription').value;
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
        questions: questions
    };

    // Send data to server (Flask back-end)
    fetch('/create-survey', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(surveyData)
    })
    .then(response => response.json())
    .then(data => {
        // Redirect to user-facing survey page
        window.location.href = `/view-survey/${data.survey_id}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
    alert('Survey Created Successfully!');
});
