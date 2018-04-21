var app = new function() {
    this.el = document.getElementById('menuItems');
    this.menuItems = ['Beef with rice', 
                    'Beef with Chapati',
                    'Beef with Ugali',
                    'Chicken with Whatever'
                    ];
    this.Count = function(data) {
        var el   = document.getElementById('counter');
        var name = 'item';
        if (data) {
            if (data > 1) {
                name = 'Menu Options';
            }
            el.innerHTML = data + ' ' + name ;
        } else {
            el.innerHTML = 'No ' + name;
        }
    };
    
    this.FetchAll = function() {
        var data = '';
        if (this.menuItems.length > 0) {
            for (i = 0; i < this.menuItems.length; i++) {
                data += '<tr>';
                data += '<td>' + this.menuItems[i] + '</td>';
                data += '<td><button onclick="app.Edit(' + i + ')">Edit</button></td>';
                data += '<td><button onclick="app.Delete(' + i + ')">Delete</button></td>';
                data += '</tr>';
            }
        }
        this.Count(this.menuItems.length);
        return this.el.innerHTML = data;
    };
    this.Add = function () {
        el = document.getElementById('add-name');
        // Get the value
        var item = el.value;
        if (item) {
            // Add the new value
            this.menuItems.push(item.trim());
            // Reset input value
            el.value = '';
            // Dislay the new list
            this.FetchAll();
        }
    };
    this.Edit = function (item) {
        var el = document.getElementById('edit-name');
        // Display value in the field
        el.value = this.menuItems[item];
        // Display fields
        document.getElementById('spoiler').style.display = 'block';
        self = this;
        document.getElementById('saveEdit').onsubmit = function() {
            // Get value
            var item = el.value;
            if (item) {
                // Edit value
                self.menuItems.splice(item, 1, item.trim());
                // Display the new list
                self.FetchAll();
                // Hide fields
                CloseInput();
            }
        }
    };
    this.Delete = function (item) {
        // Delete the current row
        this.menuItems.splice(item, 1);
        // Display the new list
        this.FetchAll();
    };
    
}
app.FetchAll();
function CloseInput() {
    document.getElementById('spoiler').style.display = 'none';
}