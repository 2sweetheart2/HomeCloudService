
function showLoader() {
  // Создаем div элемент
  const loaderDiv = document.createElement('div');
  loaderDiv.style.position = 'absolute';
  loaderDiv.style.width = '100%';
  loaderDiv.style.height = '100%';
  loaderDiv.style.background = 'rgba(0,0,0,0.8)';
  loaderDiv.style.display = 'flex';
  loaderDiv.style.flexDirection = 'row';
  loaderDiv.style.justifyContent = 'center';
  loaderDiv.style.alignItems = 'center';

  // Добавляем элемент loader внутри следующего div
  const loader = document.createElement('div');
  loader.className = 'loader';

  loaderDiv.appendChild(loader);

  // Добавляем id для идентификации и удаления элемента
  loaderDiv.id = 'loading-screen';

  // Добавляем элемент в начало body
  document.body.prepend(loaderDiv);
}

function hideLoader() {
  // Находим элемент и удаляем его
  const loaderDiv = document.getElementById('loading-screen');
  if (loaderDiv) {
    loaderDiv.remove();
  }
}

// Пример использования
// Для скрытия вызовите hideLoader(), например, после загрузки данных