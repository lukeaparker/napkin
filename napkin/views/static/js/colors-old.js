function stringToHSLColor(string, saturation = 100, lightness = 35) {
  // basic "hash" ..more like string to int conversion

  let hash = parseInt(
    string.split("").reduce((a, b) => {
      a = (a << 5) - a + b.charCodeAt(0);
      return a & a;
    }, 0),
    16
  );

  const hue = hash % 360; // keeps hue value between 0 and 360

  return `hsla(${hue}, ${saturation}%, ${lightness}%, 1)`;
}

function getInitials(name) {
  // check if first char in string is alphanumeric, otherwise cut off (since ids must be unique)
  const clean_id = /\w{1}/i.test(name.charAt(0)) ? name : name.substring(1);
  // console.log('CLEAN ID', clean_id)
  // splits name by whitespace(\s), dash(-) or comma(,)
  // returns first letter of each word up to 3 characters
  return clean_id
    .split(/['\s-,']+/)
    .map((word) => word[0])
    .join("")
    .substring(0, 3)
    .toUpperCase();
}

function setAvatar(name) {
  // sets avatar bg color based on name
  const item = document.getElementById(name);
  const initials = getInitials(item?.id);

  item?.style.setProperty("background", stringToHSLColor(item?.id, 100, 25));

  if (
    item?.classList.contains("icon-label-user") ||
    item?.classList.contains("logo")
  ) {
    item.textContent = initials;
  }
}

/* sets headers bg color based on id (to match avatar icon color) */
function setHeaderIconColor(id) {
  const item = document.getElementById(id);
  const child = document.querySelector(".icon-label-large>.iconify");

  const objectId = item?.getAttribute("data-id");
  item?.style.setProperty("background", `${stringToHSLColor(objectId)}`);
}

function setHeaderColor(id) {
  // set body to match avatar color
  const item = document.querySelector("body");

  if (id !== "search-results" && id !== "recent-searches") {
    item?.style.setProperty(
      "background",
      `linear-gradient(to top, rgba(0,0,0,0.95) 10%, ${stringToHSLColor(
        id,
        100,
        35
      )} 100%`
    );
    // document.querySelector('header')?.style.setProperty('--bg-color', `linear-gradient(to top, rgba(0,0,0,0) 0%, ${stringToHSLColor(id)} 100%`)
  } else {
    document
      .querySelector(".card-body")
      ?.style.setProperty("background", "rgba(0,0,0,0)");
  }
  // console.log(id, item?.style.background)
}

document.querySelectorAll(".icon-label-user").forEach((item) => {
  setAvatar(item.id);
});

document.querySelectorAll(".icon-label").forEach((item) => {
  // const id = item.getAttribute('data-id')
  setHeaderIconColor(item.id);
  if (item.id === `large-${item.id}`) {
    setHeaderIconColor(`large-${item.id}`);
  }
  // const initials = getInitials(item.id)
  // item.textContent = initials
});

document.querySelectorAll(".card-header").forEach((item) => {
  const id = item.getAttribute("data-id");
  setHeaderColor(id);

  if (
    item.classList.contains("organization") ||
    item.classList.contains("user")
  ) {
    const initials = getInitials(item.id);

    const child = document.querySelector(".icon-label-large");
    child.textContent = initials;
  }
});

document.querySelectorAll(".icon-label-org-user").forEach((item) => {
  const id = item.getAttribute("data-id");
  const initials = getInitials(item.id);
  item.textContent = initials;
  setAvatar(id);
});
