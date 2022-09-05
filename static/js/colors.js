// Notes on how colors are set (as of 03/23/2022):
// - HTML id attributes have to be unique, so we use `data-id` attribute to set the color with the objectId passed in from jinja

// returns a hue value for a given string
function stringToHSLColor(string, saturation = 100, lightness = 35) {
  const hash = parseInt(string.split('').reduce((a, b) => {
    a = (a << 5) - a + b.charCodeAt(0);
    return a & a % 360;
  }, 0), 16);
  // const hash = parseInt(string, 16) % 360;
  const hue = hash % 360 // keeps hue value between 0 and 360
  console.log(string, hash, hue)
  return `hsla(${hue}, ${saturation}%, ${lightness}%, 1)`
}

// set the initials of the given string
function setInitials(name) {
  // check if first char in string is alphanumeric, otherwise cut off (since ids must be unique, the janky workaround was to have '@Luke Parker' or 'Luke Parker' as id)

  const strip_symbol = /\w{1}/i.test(name.charAt(0))
    ? name
    : name.substring(1)

  // if name is more than one word, split by whitespace(\s), dash(-) or comma(,) and return first letter of each word up to 3 characters
  const initials = strip_symbol.split(/['\s-,']+/).map(word => word[0]).join('').substring(0, 3).toUpperCase()

  return initials
}

// sets the icon color based on the data-id (objectId) value
function setIconColor(id) {
  console.log('stuff', id, 'yea')

  const napkin = document.getElementById(id)
  console.log(napkin)
  const dataId = napkin.getAttribute('data-id')

  napkin?.style.setProperty('--custom-color', `${stringToHSLColor(dataId)}`)
}

// set background color of body on any single object view (views that aren't collections, like search or all users/orgs/etc)
function setBodyBackgroundColor(id) {
  const body = document.querySelector('body')
  const napkin = document.getElementById(id)
  const dataId = napkin.getAttribute('data-id')
  if (dataId) {
    body?.style.setProperty('--custom-color', `linear-gradient(to top, rgba(0,0,0,0.95) 10%, ${stringToHSLColor(dataId)} 100%`)
  } else {
    body?.style.setProperty('background', 'var(--custom-color)')
  }
}

// sets the headerIcon colors & initials for all avatar circles
document.querySelectorAll('.icon-label').forEach(napkin => {
  setIconColor(napkin.id)
  if (napkin.classList.contains('initials')) {
    napkin.textContent = setInitials(napkin.id)
  }
})


// sets the headerIcon colors & initials for all avatar circles
document.querySelectorAll('.icon-label-large').forEach(napkin => {

  const initials = napkin.id.substring(napkin.id.indexOf('-')+1)

  if (napkin.classList.contains('initials')) {
    napkin.textContent = setInitials(initials)
  }

})

document.querySelectorAll('.card-header').forEach(napkin => {
  if (napkin.id) { setBodyBackgroundColor(napkin.id) }
})
