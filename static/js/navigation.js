/* Tab Navigation
*/
const tabs = document.querySelectorAll('[data-tab-target]')
const tabContents = document.querySelectorAll('[data-tab-content]')

tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const target = document.querySelector(tab.dataset.tabTarget)
    tabContents.forEach(tabContent => {
      tabContent.classList.remove('active')
    })
    tabs.forEach(tab => {
      tab.classList.remove('active')
    })
    tab.classList.add('active')
    target.classList.add('active')
  })
})


/*
*   This content is licensed according to the W3C Software License at
*   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
*
*   Supplemental JS for the disclosure menu keyboard behavior
*/


class DropdownNav {
  constructor(node) {
    this.rootNode = node;
    this.triggerNodes = [];
    this.controlledNodes = [];
    this.openIndex = null;
    this.useArrowKeys = true;
  }
  init() {
    const buttons = this.rootNode.querySelectorAll('button[aria-expanded][aria-controls]');
    for (const i = 0; i < buttons.length; i++) {
      const button = buttons[i];
      const menu = button.parentNode.querySelector('ul');
      if (menu) {
        // save ref to button and controlled menu
        this.triggerNodes.push(button);
        this.controlledNodes.push(menu);

        // collapse menus
        button.setAttribute('aria-expanded', 'false');
        this.toggleMenu(menu, false);

        // attach event listeners
        menu.addEventListener('keydown', this.handleMenuKeyDown.bind(this));
        button.addEventListener('click', this.handleButtonClick.bind(this));
        button.addEventListener('keydown', this.handleButtonKeyDown.bind(this));
      }
    }

    this.rootNode.addEventListener('focusout', this.handleBlur.bind(this));
  }
  toggleMenu(node, show) {
    if (node) {
      node.style.display = show ? 'block' : 'none';
    }
  }
  toggleExpand(index, expanded) {
    // close open menu, if applicable
    if (this.openIndex !== index) {
      this.toggleExpand(this.openIndex, false);
    }

    // handle menu at called index
    if (this.triggerNodes[index]) {
      this.openIndex = expanded ? index : null;
      this.triggerNodes[index].setAttribute('aria-expanded', expanded);
      this.toggleMenu(this.controlledNodes[index], expanded);
    }
  }
  controlFocusByKey(keyboardEvent, nodeList, currentIndex) {
    switch (keyboardEvent.key) {
      case 'ArrowUp':
      case 'ArrowLeft':
        keyboardEvent.preventDefault();
        if (currentIndex > -1) {
          const prevIndex = Math.max(0, currentIndex - 1);
          nodeList[prevIndex].focus();
        }
        break;
      case 'ArrowDown':
      case 'ArrowRight':
        keyboardEvent.preventDefault();
        if (currentIndex > -1) {
          const nextIndex = Math.min(nodeList.length - 1, currentIndex + 1);
          nodeList[nextIndex].focus();
        }
        break;
      case 'Home':
        keyboardEvent.preventDefault();
        nodeList[0].focus();
        break;
      case 'End':
        keyboardEvent.preventDefault();
        nodeList[nodeList.length - 1].focus();
        break;
    }
  }
  /* Event Handlers */
  handleBlur(event) {
    const menuContainsFocus = this.rootNode.contains(event.relatedTarget);
    if (!menuContainsFocus && this.openIndex !== null) {
      this.toggleExpand(this.openIndex, false);
    }
  }
  handleButtonKeyDown(event) {
    const targetButtonIndex = this.triggerNodes.indexOf(document.activeElement);

    // close on escape
    if (event.key === 'Escape') {
      this.toggleExpand(this.openIndex, false);
    }


    // move focus into the open menu if the current menu is open
    else if (this.useArrowKeys && this.openIndex === targetButtonIndex && event.key === 'ArrowDown') {
      event.preventDefault();
      this.controlledNodes[this.openIndex].querySelector('a').focus();
    }


    // handle arrow key navigation between top-level buttons, if set
    else if (this.useArrowKeys) {
      this.controlFocusByKey(event, this.triggerNodes, targetButtonIndex);
    }
  }
  handleButtonClick(event) {
    const button = event.target;
    const buttonIndex = this.triggerNodes.indexOf(button);
    const buttonExpanded = button.getAttribute('aria-expanded') === 'true';
    this.toggleExpand(buttonIndex, !buttonExpanded);
  }
  handleMenuKeyDown(event) {
    if (this.openIndex === null) {
      return;
    }

    const menuLinks = Array.prototype.slice.call(this.controlledNodes[this.openIndex].querySelectorAll('a'));
    const currentIndex = menuLinks.indexOf(document.activeElement);

    // close on escape
    if (event.key === 'Escape') {
      this.triggerNodes[this.openIndex].focus();
      this.toggleExpand(this.openIndex, false);
    }


    // handle arrow key navigation within menu links, if set
    else if (this.useArrowKeys) {
      this.controlFocusByKey(event, menuLinks, currentIndex);
    }
  }
  // switch on/off arrow key navigation
  updateKeyControls(useArrowKeys) {
    this.useArrowKeys = useArrowKeys;
  }
}
