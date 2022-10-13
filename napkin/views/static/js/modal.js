/**
 * REF: https://levelup.gitconnected.com/an-accessible-modal-dialog-with-html-css-and-javascript-d885004d0b3a
 * REF: https://www.smashingmagazine.com/2021/07/accessible-dialog-from-scratch/
 * */

const modal = {
  callOpen: () => {
    modal.opener = document.activeElement;
    // console.log("Opening: " + modal.opener.id);
    openModal(modal.opener.id);
  },
  callClose: () => {
    closeModal(modal.opener.id);
  },

  // Add statement to exclude recommended search clicks

  // handleOverlayClick: (event) => {
  //   // if not click inside modal, close modal
  //   if (!event.target.closest('.modal')) {

  //     closeModal(modal.opener.id)
  //   }
  // }
};

function openModal(id) {
  setVisible(true, id);
  setFocus(id);
  setInertBehindModal(true);
}

function closeModal(id) {
  setVisible(false, id);
  setInertBehindModal(false);
  // console.log("beep");
  // opener.focus()
}

function attachEventListener(openButtons, closeButtons, overlay) {
  openButtons.forEach((b) => {
    b.addEventListener("click", modal.callOpen);
  });
  closeButtons.forEach((b) => {
    b.addEventListener("click", modal.callClose);
  });
  overlay.addEventListener("click", modal.handleOverlayClick);
  window.addEventListener("keydown", callIfEscPress);
}

function setVisible(visible, id) {
  const display = visible ? "flex" : "none";

  document.querySelector(".overlay").style.display = display;
  const modalType = id.slice(0, id.indexOf("-button"));
  // console.log(modalType);

  document.querySelector(`#${modalType}`).style.display = display;

  document.querySelectorAll(".modal").forEach((modal) => {
    if (modal.id !== modalType) {
      document.getElementById(modal.id).style.display = "none";
      // console.log("open", modal.id);
    } else {
      document.getElementById(modal.id).style.display = "flex";
      // console.log("close", modal.id);
    }
  });
}

function setFocus(id) {
  // document.querySelectorAll('.modal button, modal input, modal textarea, modal select')[0].focus()
  document.querySelector(`#${id}`).focus();
}

function setInertBehindModal(inert) {
  const element = document.querySelector("main");
  element.inert = inert;
 element.setAttribute("aria-hidden", inert);
}

function callIfEscPress(event) {
  if (event.key === "Escape") {
    modal.callClose();
  }
}

const openButtons = document.querySelectorAll(".open-modal");
const closeButtons = document.querySelectorAll(".close-modal");
const overlay = document.querySelector(".overlay");
attachEventListener(openButtons, closeButtons, overlay);
