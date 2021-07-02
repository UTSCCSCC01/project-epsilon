// currently no import works
// import React  from 'react';
// import ReactDOM from 'react-dom';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import Card from "react-bootstrap/Card";


class CompanyRow extends React.Component {
    render() {
        const name = this.props.name;
        const description = this.props.description;
        // const industry = this.props.industry;
        return (
            <tr>
                <td>{name}</td>
                <td>{description}</td>
                {/*<td>{industry}</td>*/}
            </tr>
        );
    }
}

class CompanyTable extends React.Component {
    render() {
        const rows = [];
        this.props.company_list.forEach((company) => {
                rows.push(
                    <CompanyRow
                        name={company.name}
                        description={company.description}
                        // industry={company.industry.toString()}
                    />
                );
        });
        return (
            <div>
                {/*<Card>*/}
                {/*    <Card.Body>This is some text within a card body.</Card.Body>*/}
                {/*</Card>*/}

            <table>
                <thead>
                <tr>
                    <th>name</th>
                    <th>description</th>
                    {/*<th>industry</th>*/}
                </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
            </div>

        );
    }
}

class SearchResult extends React.Component {
    constructor(props) {
        super(props);
    }

    render(){
        const styles={ position: 'relative',top: 100,padding: "10px 20px", textAlign: "center"};
        return (

            <div style={styles}>
                <CompanyTable
                    company_list={this.props.company_list}
                />
            </div>
        );
    }
}

class Error extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div>{alert(this.props.error.message)}</div>
        );
    }
}

// const domContainer = document.querySelector('#search_page');
if (typeof company_data !== 'undefined'){
    const cd = company_data.company_list;
    ReactDOM.render(<SearchResult company_list={cd}/>, document.getElementById('search_page'));
}else if (typeof error !== 'undefined') {
    const e = error;
    ReactDOM.render(<Error error={e}/>, document.getElementById('search_page'));
}