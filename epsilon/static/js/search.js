class SearchBar extends React.Component {
    constructor() {
        super();
        for (let i = 0; i < company_data.company_list.length; i++) {
            console.log(i);
            const inner = company_data.company_list[i];
            console.log(inner["name"]);
            console.log(inner["description"]);
            console.log(inner["industry"]);
        }
    }

    render() {
        return (
                <form>
                    <input
                        type="text"
                        placeholder="Search..."/>
                    <p>{company_data.company_list[0]["description"]}</p>
                </form>
        );
    }
}

// const domContainer = document.querySelector('#search_page');
ReactDOM.render(<SearchBar/>, document.getElementById('search_page'));
