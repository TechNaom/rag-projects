document.addEventListener('DOMContentLoaded', () => {
  const questions = [...document.querySelectorAll('.quiz-question')];
  const progressBar = document.querySelector('.progress-bar');
  const progressCopy = document.querySelector('.progress-copy');

  const updateProgress = () => {
    const solved = questions.filter((question) => question.dataset.correct === 'true').length;
    const percent = questions.length ? Math.round((solved / questions.length) * 100) : 0;
    if (progressBar) progressBar.style.width = `${percent}%`;
    if (progressCopy) progressCopy.textContent = `${solved} of ${questions.length} correct`;
    if (percent === 100 && document.body.dataset.quizKey) {
      localStorage.setItem(document.body.dataset.quizKey, 'completed');
    }
  };

  questions.forEach((question) => {
    const input = question.querySelector('input[data-answer]');
    const button = question.querySelector('.check-answer');
    const feedback = question.querySelector('.quiz-feedback');
    if (!input || !button || !feedback) return;
    button.addEventListener('click', () => {
      const expected = input.dataset.answer.trim().toLowerCase();
      const actual = input.value.trim().toLowerCase();
      const ok = actual === expected;
      question.dataset.correct = ok ? 'true' : 'false';
      feedback.textContent = ok ? '✅ Correct' : `❌ Try again — expected ${input.dataset.answer}`;
      feedback.className = `quiz-feedback ${ok ? 'correct' : 'incorrect'}`;
      updateProgress();
    });
  });

  updateProgress();
});
