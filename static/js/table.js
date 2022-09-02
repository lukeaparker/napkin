

function updateRank(action, rank) {
  const object_id = document.getElementById('object').dataset.id

  const url = `/api/${action}/object/attribute/${object_id}/${rank}`

  fetch(url, {
    headers: {
      method: 'GET',
      'content-type': 'application/json'
    }
  })
    .then(response =>
      // console.log(response.json())
    )
}

function swap(item1, item2) {
  const parent = item1.parentNode

  parent.insertBefore(item1, item2)

}

document.querySelectorAll('[data-reorder]').forEach(element => {

  element.addEventListener('click', (event) => {
    let action = event.currentTarget.getAttribute('data-reorder')
    let rank = event.currentTarget.getAttribute('data-rank')
    let row = document.querySelector(`#attr-${rank}`)
    let sibling
    // console.log('click -> ', action, typeof (rank))
    switch (action) {
      case 'increment':
        sibling = row.previousElementSibling

        swap(row, sibling)
        // console.log(action, row, sibling)
        break
      case 'decrement':
        sibling = row.nextElementSibling
        swap(sibling, row)
        // console.log(action, row, sibling)
        break
      default:
        return
    }
    updateRank(action, rank)
  })
})
