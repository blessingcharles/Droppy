// Add event with callback function to each item in the HTML Collection.
function addEventsToCollection (configObj, callback) {
    const event = configObj.event
    const collection = configObj.collection
  
    if (collection.length) {
      Array.prototype.map.call(collection, function (index) {
        return index.addEventListener(event, callback)
      })
    } else {
      console.log('TABLE.JS: HTML collection not present.')
      return false  // No table headers on this page; prevent undefined.
    }
  }
  
  // When table headers are clicked (targeted by classname), toggle the collapsed / expanded class name.
  // Expanded by default.
  addEventsToCollection({
    event: 'click',
    collection: document.getElementsByClassName('table-header')
  }, function (event) {
    let element = ''
    // I'm making an assumption that the header will be an adjacent sibling
    // to the table and that the clickable element will be a header or a button.
    if (event.target.nodeName === 'BUTTON') {
      element = event.target.parentNode
    } else if (event.target.nodeName === 'H3') {
      element = event.target
    } else {
      return false
    }
    // Toggle the header classes.
    element.classList.toggle('table-header--expanded')
    element.classList.toggle('table-header--collapsed')
    // Toggle the table classes & states.
    element.nextElementSibling.hidden ? element.nextElementSibling.removeAttribute('hidden') : element.nextElementSibling.hidden = 'true'
    element.nextElementSibling.classList.toggle('table--expanded')
    element.nextElementSibling.classList.toggle('table--collapsed')
  })