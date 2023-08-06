from datawidgets.imports import *
from datawidgets.ui import *
from datawidgets.data.image import *


class ImageLoaderMixin:
    def setup_img(self):
        # Create image widget
        self.img = widgets.Image(value=self.load_img_bytes(), width=f"100%")
        self.img.add_class(CSS_NAMES.IMG_BOX)

    def load_img_bytes(self):
        if "https://" in self.source:
            return requests.get(self.source).content
        else:
            return Path(self.source).read_bytes()


class ClassificationLabelsMixin:
    """
    Three points where updating of labels happens:
      1. `self.add_label`
      2. `self.remove_label`
      3. when any of `self.label_buttons` is clicked

    The updating logic is defined in `self.update_dataset()`, which is called
    during both (1) and (2), and is passed as a callback to (3) on init
    """

    _works_with = "ImageWithLabels"

    def setup_labelling(self):
        self.is_modified = False
        self.label_buttons = ClassificationLabelButtons(
            class_map=self.class_map,
            labels=self._labels,
            callbacks=[
                self.monitor_searchbox_status,
                self.remove_label,
            ],
        )
        self.searchbox = Dropdown(
            options=self.classes + [""],
            value="",
            layout=CSS_LAYOUTS.flex_layout,
        )
        self.searchbox.add_class(CSS_NAMES.LABEL_SEARCH_BOX)
        self.searchbox.observe(self.monitor_searchbox_value)

        self.monitor_searchbox_status()

    @property
    def labels(self):
        return self.label_buttons.labels

    @property
    def max_labels_selected(self):
        if not self.is_multilabel and len(self.labels) == 1:
            return True
        return False

    def monitor_searchbox_status(self, change=None):
        if self.max_labels_selected:
            self.searchbox.disabled = True
        else:
            self.searchbox.disabled = False

    def monitor_searchbox_value(self, change):
        if self.searchbox.value != "" and self.searchbox.value in self.classes:
            self.add_label(self.searchbox.value)

            # empty the searchbox if a full, unique label is entered (and assigned)
            # if sum([l.startswith(self.searchbox.value) for l in self.classes]) == 1:
            #     self.searchbox.value = ""

            self.searchbox.value = ""
        self.monitor_searchbox_status()

    def update_dataset(self, *args):
        self.is_modified = True
        if self.dset is not None:
            if self.is_multilabel:
                # Pandas throws a `ValueError` if `self.labels` if of different
                # length than the previous value. See https://stackoverflow.com/questions/48000225/must-have-equal-len-keys-and-value-when-setting-with-an-iterable
                # To get around this, we have to
                #  get a copy of the row -> mutate in place -> delete old row -> set new row
                row = self.dset.df.loc[self.source]
                row.at[self.dset.label_col] = self.labels
                row = pd.DataFrame(row).T
                row.set_index(row.filename, inplace=True)

                self.dset.df = self.dset.df.drop(self.source).append(row)

            else:
                self.dset.df.at[self.source, self.dset.label_col] = self.labels
            self.log_message(f"Altered {self.source}'s labels...?")

    def add_label(self, label: str):
        self.label_buttons.append(label)
        self.update_dataset()

    def remove_label(self, label: str):
        self.label_buttons.remove(label)
        self.update_dataset()


class ImageMouseInteractionMixin:
    """Defines mouse click and hover interaction for `ImageWithLabels`

    * Adds `self.class_on_hover` as a DOM class when the mouse hovers over the image
    * Adds `self.class_on_click` as a DOM class when the image is clicked
    """

    is_selected = False

    # For `select` and `unselect`, it makes more sense to have
    #  the entire display box selected rather than just the image...
    def select(self):
        "Behavior the image is selected (on click)"
        self.is_selected = True
        # self.view.add_class(CSS_NAMES.IMG_BOX_CONTAINER_SELECTED)
        self.img.add_class(CSS_NAMES.IMG_BOX_SELECTED)

    def unselect(self):
        "Behavior the image is de-selected (on click)"
        self.is_selected = False
        # self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER_SELECTED)
        self.img.remove_class(CSS_NAMES.IMG_BOX_SELECTED)

    def setup_mouse_interaction(self):
        "Create the `ipyevent` and attaches it to `self.img`"
        self.is_selected = False
        ev = Event(
            source=self.img, watched_events=["click", "mouseenter", "mouseleave"]
        )
        ev.on_dom_event(self.mouse_interaction_img)

    def mouse_interaction_img(self, event):
        "Defines mouse hover and click interaction"
        if event["type"] == "mouseenter":
            if not self.is_selected:
                self.img.add_class(CSS_NAMES.IMG_BOX_HOVER)
                self.log_message("Mouse entered image region")

        elif event["type"] == "mouseleave":
            if not self.is_selected:
                self.img.remove_class(CSS_NAMES.IMG_BOX_HOVER)
                self.log_message("Mouse left image region")

        elif event["type"] == "click":
            if not self.is_selected:
                self.select()
                self.log_message("Mouse clicked, image selected")
            elif self.is_selected:
                self.unselect()
                self.log_message("Mouse clicked, image UN-selected")
