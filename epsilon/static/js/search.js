class SearchBar extends React.Component {
    constructor() {
        super();
        if (typeof company_data !== 'undefined'){
            for (let i = 0; i < company_data.company_list.length; i++) {
                console.log(i);
                const inner = company_data.company_list[i];
                console.log(inner["name"]);
                console.log(inner["description"]);
                console.log(inner["industry"]);
            }
        }
    }

    render() {
        return (
            <div>
                <p>
                    render complete
                </p>
            </div>
        );
    }
}

// const domContainer = document.querySelector('#search_page');
ReactDOM.render(<SearchBar/>, document.getElementById('search_page'));
