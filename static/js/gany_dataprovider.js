var gany = gany || {};

$.extend( gany, (function() {

    function Row( _layout, _data ) {
        var data = _data;
        var layout = _layout;

        var render = function() {
            return $.tmpl( layout, data );
        }

        return {
            "render" : render
        }
    }

    function Table( _el, _provider ) {
        this.el = _el;
        this.provider = _provider;

        var that = this;
        $( this.provider ).on( "data-changed", function() {
            that.render();
        } );

        this.render = function() {
            var def = this.provider.get_data();
            var that = this;
            def.done( function( data ) {
                var rows = [];
                for ( x in data ) {
                    rows.push( new Row( "test_layout", data[ x ] ) );
                }
                that.el.html("");
                for ( x in rows ) {
                    that.el.append( rows[x].render() );
                }
            });
            $('[data-toggle="tooltip"]').tooltip();
            return def;
        }

        return this;
    }

    function DataProvider( _data, _filters, _orders, _pagination ) {
        this.data = _data;
        this.filters = _filters || [];
        this.orders = _orders || [];
        this.pagination = _pagination || { page:1, pageSize:20 };
        this.check = function ( id ) {
            this.checkedlist.add( id );
        }

        this.uncheck = function ( id ) {
            this.checkedlist.remove( id );
        }

        this.checkedlist = new gany.dataprovider.TestList( [] );
        for ( x in this.data ) {
            if ( this.data[ x ].checked ) {
                this.checkedlist.add( this.data[ x ].id );
            }
            this.data[ x ].checked = false;
        }

        this.get_data = function () {
            var c_data = this.data;
            for ( x in this.filters ) {
                c_data = this.filters[ x ].apply( c_data );
            }
            for ( x in this.orders ) {
                c_data = this.orders[ x ].apply( c_data );
            }

            this.pagination.totalPages = Math.floor( (c_data.length - 1) / this.pagination.pageSize ) + 1;

            c_data = c_data.slice(
                (this.pagination.page - 1) * this.pagination.pageSize,
                this.pagination.page * this.pagination.pageSize
            );

            for (x in c_data) {
                c_data[x].checked = this.checkedlist.contains( c_data[x].id );
            }

            var def = $.Deferred();
            def.resolve( c_data );
            return def;
        }

        return this;
    }

    function FilterProto() {
        return {
            apply : function( data ) {
                var res = [];
                for ( x in data ) {
                    if ( this.one( data[ x ] ) ) {
                        res.push( data[ x ] );
                    }
                }
                return res;
            }
        }
    }

    function LikeFilter( _attr, _like ) {
        this.like = _like;
        this.attr = _attr;
        this.one = function ( item ) {
            return item[ this.attr ].indexOf( this.like ) != -1;
        }
        return this;
    }

    function ParentFilter( _attr, _val ) {
        this.val = _val;
        this.attr = _attr;
        this.one = function ( item ) {
            return  this.val == '' || item[ "parent_id" ] == this.val || item[ "id" ] == this.val;
        }
        return this;
    }

    LikeFilter.prototype = FilterProto();
    ParentFilter.prototype = FilterProto();

    function Pagination( _prev, _next, _page, _provider ) {
        this.prev = _prev;
        this.next = _next;
        this.page = _page;
        this.provider = _provider;

        var that = this;

        $( that.provider ).on( "data-changed", function() {
            that.render();
        } );

        this.prev.click(function() {
            var x = that.provider.pagination;
            if (x.page > 1)
                x.page = x.page * 1 - 1;

            $(that.provider).trigger( "data-changed" );
            return false;
        });

        this.next.click(function() {
            if (that.next.parents("li").hasClass('disabled'))
                return false;
            var x = that.provider.pagination;
            x.page = x.page * 1 + 1;

            $(that.provider).trigger( "data-changed" );
            return false;
        });

        this.render = function() {
            var x = that.provider.pagination;
            if (x.page == x.totalPages) {
                this.next.parents("li").addClass("disabled");
            } else {
                this.next.parents("li").removeClass("disabled");
            }
            if (x.page == 1) {
                this.prev.parents("li").addClass("disabled");
            } else {
                this.prev.parents("li").removeClass("disabled");
            }
            this.page.text( x.page + " из " + x.totalPages );
        }
    }

    function TestsList( _tests ) {
        this.tests = _tests;
        this.remove = function ( id ) {
            for ( x in this.tests ) {
                if ( this.tests[ x ] == id ) {
                    delete this.tests[ x ];
                }
            }
        };
        this.add = function ( id ) {
            if (!this.contains( id )) {
                this.tests.push( id );
            }
        };
        this.contains = function ( id ) {
            for ( x in this.tests ) {
                if ( this.tests[ x ] == id ) {
                    return true;
                }
            }
            return false;
        };
        this.all = function () {
            var res = [];
            for (x in this.tests) {
                if (this.tests[x]) {
                    res.push( this.tests[x] );
                }
            }
            return res;
        }
        return this;
    }

    var storage = {};
    function global( name, data ) {
        if (!data) {
            return storage[ name ];
        } else {
            storage[ name ] = data;
        }
    }

    return {
        "dataprovider" : {
            Row : Row,
            Table : Table,
            DataProvider : DataProvider,
            LikeFilter : LikeFilter,
            ParentFilter : ParentFilter,
            Pagination : Pagination,
            TestList : TestsList,
            global : global
        }
    };

})() );